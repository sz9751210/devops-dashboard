from app.controllers.link_list_controller import LinkListController
from app.controllers.event_controller import EventController

def setup_routes(app, db):
    link_list_controller = LinkListController(db)
    event_controller = EventController(db)
    
    api_prefix= '/api'
    
    app.add_url_rule(f"{api_prefix}/devops/link-list", view_func=link_list_controller.get_link_list, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/devops/event", view_func=event_controller.get_event, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/devops/event", view_func=event_controller.post_event, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/devops/event/<event_id>", view_func=event_controller.update_event, methods=['PUT'])
    app.add_url_rule(f"{api_prefix}/devops/event/<event_id>", view_func=event_controller.delete_event, methods=['DELETE'])