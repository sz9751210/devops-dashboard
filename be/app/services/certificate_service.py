import ssl
import socket
import time
from multiprocessing import Pool
from datetime import datetime
from app.utils.cloudflare import CloudflareManager
from config.config import Config


class CertificateService:
    def __init__(self, client):
        db = client['it']
        self.collection = db['cert']

    def get_domain_list(self):
        domains = list(self.collection.find({}))
        for domain in domains:
            for subdomain in domain.get('subdomains', []):
                subdomain['status'] = bool(subdomain['status'])
        return domains

    def get_ssl_cert_info(self, domain, retries=3, delay=3, timeout=2.0):
        ssl_context = ssl.create_default_context()
        for attempt in range(retries):
            with ssl_context.wrap_socket(
                socket.socket(socket.AF_INET), server_hostname=domain
            ) as conn:
                conn.settimeout(timeout)
                try:
                    conn.connect((domain, 443))
                    return conn.getpeercert()
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed for {domain}: {e}")
                    if attempt < retries - 1:
                        time.sleep(delay)
                    else:
                        return None

    def parse_ssl_cert_info(self, domain, cert):
        if cert is None:
            return {"error": f"無法取得 {domain} 的 SSL 證書資訊"}

        issuer = dict(x[0] for x in cert["issuer"])
        subject = dict(x[0] for x in cert["subject"])
        issued_to = subject.get(
            "commonName", subject.get("organizationName", ""))
        issued_by = issuer.get(
            "commonName", issuer.get("organizationName", ""))
        valid_from = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z").strftime(
            "%Y-%m-%d"
        )
        valid_until = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").strftime(
            "%Y-%m-%d"
        )

        return {
            "domain": domain,
            "issuedTo": issued_to,
            "issuedBy": issued_by,
            "validFrom": valid_from,
            "validUntil": valid_until
        }

    def update_domain_status(self, domain, subdomain, status):
        result = self.collection.update_one(
            {"domain": domain, "subdomains.name": subdomain},
            {"$set": {"subdomains.$.status": status}}
        )
        return result.modified_count > 0

    def sync_cloudflare_records(self):
        try:
            # Fetch all domains and DNS records from Cloudflare
            cloudflare_manager = CloudflareManager(
                api_key=Config.CLOUDFLARE_API_KEY, email=Config.CLOUDFLARE_EMAIL)
            domain_tuples = cloudflare_manager.fetch_all_domains_and_records()

            # Convert to dictionary format
            new_domains = self.convert_domains_to_dict(domain_tuples)
            print(f"New domains: {new_domains}")  # 添加調試日誌

            # Fetch current domains from DB
            current_domains = self.get_domain_list()
            current_domains_dict = {
                domain['domain']: domain['subdomains'] for domain in current_domains}
            print(f"Current domains: {current_domains_dict}")  # 添加調試日誌

            # Current date for update_date field
            current_date = datetime.now().strftime("%Y-%m-%d")

            # Prepare data for DB update
            self.update_existing_domains(
                new_domains, current_domains_dict, current_date)
            self.insert_new_domains(
                new_domains, current_domains_dict, current_date)

            return new_domains

        except Exception as e:
            print(f"Error syncing Cloudflare records: {e}")  # 添加異常日誌
            raise

    def update_existing_domains(self, new_domains, current_domains_dict, current_date):
        for domain, subdomains in new_domains.items():
            if domain in current_domains_dict:
                existing_subdomains = {sub['name']
                                       for sub in current_domains_dict[domain]}
                self.add_new_subdomains(
                    domain, subdomains, existing_subdomains, current_date)
                self.remove_old_subdomains(
                    domain, subdomains, current_domains_dict)

    def convert_domains_to_dict(self, domain_tuples):
        domain_dict = {}
        for main_domain, subdomain in domain_tuples:
            if main_domain in domain_dict:
                domain_dict[main_domain].append(subdomain)
            else:
                domain_dict[main_domain] = [subdomain]
        return domain_dict

    def add_new_subdomains(self, domain, subdomains, existing_subdomains, current_date):
        subdomains_to_add = []

        for subdomain in subdomains:
            if subdomain not in existing_subdomains:
                subdomains_to_add.append(domain, subdomain, current_date)

        with Pool() as pool:
            pool.starmap(self._process_subdomain, subdomains_to_add)

    def _process_subdomain(self, domain, subdomain, current_date):
        cert = self.get_ssl_cert_info(subdomain)
        cert_info = self.parse_ssl_cert_info(subdomain, cert)
        expiry_date = cert_info.get('validUntil') if cert_info else None
        self.collection.update_one(
            {"domain": domain},
            {"$push": {"subdomains": {"name": subdomain, "status": True,
                                      "expiry_date": expiry_date, "update_date": current_date}}}
        )

    def remove_old_subdomains(self, domain, subdomains, current_domains_dict):
        subdomains_to_remove = []
        for sub in current_domains_dict[domain]:
            if sub['name'] not in subdomains:
                subdomains_to_remove.append((domain, sub['name']))
        
        with Pool() as pool:
            pool.starmap(self._remove_subdomain, subdomains_to_remove)

    def _remove_subdomain(self, domain, subdomain):
        self.collection.update_one(
            {"domain": domain},
            {"$pull": {"subdomains": {"name": subdomain}}}
        )

    def insert_new_domains(self, new_domains, current_domains_dict, current_date):
        for domain, subdomains in new_domains.items():
            if domain not in current_domains_dict:
                subdomain_list = []
                for sub in subdomains:
                    cert = self.get_ssl_cert_info(sub)
                    cert_info = self.parse_ssl_cert_info(sub, cert)
                    expiry_date = cert_info.get(
                        'validUntil') if cert_info else None
                    subdomain_list.append(
                        {"name": sub, "status": True, "expiry_date": expiry_date, "update_date": current_date})
                self.collection.insert_one({
                    "domain": domain,
                    "subdomains": subdomain_list
                })
