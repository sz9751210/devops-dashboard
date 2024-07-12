from app.controllers.link_list_controller import LinkListController
from app.controllers.event_controller import EventController
from app.controllers.domain_controller import DomainController

def setup_routes(app, client):
    link_list_controller = LinkListController(client)
    event_controller = EventController(client)
    domain_controller = DomainController(client)
    
    api_prefix= '/api'
    
    app.add_url_rule(f"{api_prefix}/devops/link-list", view_func=link_list_controller.get_link_list, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/devops/event", view_func=event_controller.get_event, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/devops/event", view_func=event_controller.post_event, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/devops/event/<event_id>", view_func=event_controller.update_event, methods=['PUT'])
    app.add_url_rule(f"{api_prefix}/devops/event/<event_id>", view_func=event_controller.delete_event, methods=['DELETE'])
    app.add_url_rule(f"{api_prefix}/devops/domains", view_func=domain_controller.get_domains, methods=['GET'])
