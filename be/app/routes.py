from app.controllers.link_list_controller import LinkListController
from app.controllers.event_controller import EventController
from app.controllers.certificate_controller import CertificateController

def setup_routes(app, client):
    link_list_controller = LinkListController(client)
    event_controller = EventController(client)
    certificate_controller = CertificateController(client)
    
    api_prefix= '/api/devops'
    
    app.add_url_rule(f"{api_prefix}/link-list", view_func=link_list_controller.get_link_list, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/event", view_func=event_controller.get_event, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/event", view_func=event_controller.post_event, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/event/<event_id>", view_func=event_controller.update_event, methods=['PUT'])
    app.add_url_rule(f"{api_prefix}/event/<event_id>", view_func=event_controller.delete_event, methods=['DELETE'])
    app.add_url_rule(f"{api_prefix}/certificate/domains", view_func=certificate_controller.get_domains, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/certificate/check", view_func=certificate_controller.get_certificate, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/certificate/domain-status", view_func=certificate_controller.update_domain_status, methods=['PUT'])
