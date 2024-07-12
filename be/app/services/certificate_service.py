import ssl
import socket
import time
from datetime import datetime


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

    def get_ssl_cert_info(self, domain, retries=5, delay=4, timeout=5.0):
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
