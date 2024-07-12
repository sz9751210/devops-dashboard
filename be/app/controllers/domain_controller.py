from flask import jsonify
from app.services.domain_service import DomainService

class DomainController:
    def __init__(self, db):
        self.domain_service = DomainService(db)

    def get_domains(self):
        domain_list = self.domain_service.get_domain_list()
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