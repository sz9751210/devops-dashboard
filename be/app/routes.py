from app.controllers.link_list_controller import LinkListController
from app.controllers.event_controller import EventController
from app.controllers.certificate_controller import CertificateController
from app.controllers.auth_controller import AuthController
from app.controllers.setting_controller import SettingController

def setup_routes(app, client):
    link_list_controller = LinkListController(client)
    event_controller = EventController(client)
    certificate_controller = CertificateController(client)
    auth_controller = AuthController(client)
    setting_controller = SettingController(client)
    
    api_prefix= '/api/devops'
    
    app.add_url_rule(f"{api_prefix}/link-list", view_func=link_list_controller.get_link_list, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/event", view_func=event_controller.get_event, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/event", view_func=event_controller.post_event, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/event/<event_id>", view_func=event_controller.update_event, methods=['PUT'])
    app.add_url_rule(f"{api_prefix}/event/<event_id>", view_func=event_controller.delete_event, methods=['DELETE'])
    app.add_url_rule(f"{api_prefix}/certificate/domains", view_func=certificate_controller.get_domains, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/certificate/check", view_func=certificate_controller.get_certificate, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/certificate/domain-status", view_func=certificate_controller.update_domain_status, methods=['PUT'])
    app.add_url_rule(f"{api_prefix}/certificate/sync-cloudflare", view_func=certificate_controller.sync_cloudflare, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/certificate/check-subdomains", view_func=certificate_controller.check_subdomains, methods=['POST'])
    
    # auth
    app.add_url_rule(f"{api_prefix}/auth/register", view_func=auth_controller.register, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/auth/login", view_func=auth_controller.login, methods=['POST'])
    
    # Settings routes
    app.add_url_rule(f"{api_prefix}/settings", view_func=setting_controller.get_settings, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/settings", view_func=setting_controller.add_setting, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/settings/<setting_id>", view_func=setting_controller.update_setting, methods=['PUT'])
    app.add_url_rule(f"{api_prefix}/settings/<setting_id>", view_func=setting_controller.delete_setting, methods=['DELETE'])
