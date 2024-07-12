from flask import jsonify, request
from app.services.certificate_service import CertificateService


class CertificateController:
    def __init__(self, db):
        self.certificate_service = CertificateService(db)

    def get_domains(self):
        domain_list = self.certificate_service.get_domain_list()
        formatted_domain_list = self.format_domain_list(domain_list)
        return jsonify({"code": 200, "message": "success", "data": formatted_domain_list})

    def format_domain_list(self, domain_list):
        formatted_list = []
        for domain in domain_list:
            domain_info = {
                "domain": domain["domain"],
                "subdomains": []
            }
            for subdomain in domain["subdomains"]:
                domain_info["subdomains"].append({
                    "name": subdomain.get("name"),
                    "check": subdomain.get("check"),
                    "expiry_date": subdomain.get("expiry_date").isoformat() if subdomain.get("expiry_date") else None,
                    "update_time": subdomain.get("update_time").isoformat() if subdomain.get("update_time") else None
                })
            formatted_list.append(domain_info)
        return formatted_list

    def get_certificate(self):
        domain = request.args.get('domain')
        print(domain)
        if not domain:
            return jsonify({"code": 400, "message": "請提供域名"}), 400
        cert = self.certificate_service.get_ssl_cert_info(domain)
        cert_info = self.certificate_service.parse_ssl_cert_info(domain, cert)
        return jsonify({"code": 200, "message": "success", "data": cert_info})
