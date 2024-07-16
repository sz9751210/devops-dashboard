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
                    "status": subdomain.get("status"),
                    "expiry_date": subdomain.get("expiry_date") if subdomain.get("expiry_date") else None,
                    "update_time": subdomain.get("update_time") if subdomain.get("update_time") else None
                })
            formatted_list.append(domain_info)
        return formatted_list

    def format_date(self, date):
        if date:
            return datetime.strptime(date.isoformat(), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
        return None

    def get_certificate(self):
        domain = request.args.get('domain')
        if not domain:
            return jsonify({"code": 400, "message": "請提供域名"}), 400
        cert = self.certificate_service.get_ssl_cert_info(domain)
        cert_info = self.certificate_service.parse_ssl_cert_info(domain, cert)
        return jsonify({"code": 200, "message": "success", "data": cert_info})

    def update_domain_status(self):
        data = request.get_json()
        domain = data.get('domain')
        subdomain = data.get('subdomain')
        status = data.get('status')

        if not domain or not subdomain or status is None:
            return jsonify({"code": 400, "message": "請提供完整的數據"}), 400

        success = self.certificate_service.update_domain_status(domain, subdomain, status)

        if success:
            return jsonify({"code": 200, "message": "域名狀態更新成功"})
        else:
            return jsonify({"code": 500, "message": "域名狀態更新失敗"}), 500
