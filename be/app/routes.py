from app.controllers.link_list_controller import LinkListController
from app.controllers.event_controller import EventController
from app.controllers.document_controller import DocumentController
from app.controllers.certificate_controller import CertificateController
from app.controllers.auth_controller import AuthController
from app.controllers.setting_controller import SettingController
from app.controllers.cronjob_controller import CronjobController
from app.controllers.operation_log_controller import OperationLogController

def setup_routes(app, client, scheduler):

    # controllers
    link_list_controller = LinkListController(client)
    event_controller = EventController(client)
    document_controller = DocumentController(client)
    certificate_controller = CertificateController(client)
    auth_controller = AuthController(client)
    setting_controller = SettingController(client)
    cronjob_controller = CronjobController(client, scheduler)
    operation_log_controller = OperationLogController(client)

    api_prefix= '/api/devops'
    
    # link-list
    app.add_url_rule(f"{api_prefix}/link-list", view_func=link_list_controller.get_link_list, methods=['GET'])

    # event
    app.add_url_rule(f"{api_prefix}/event", view_func=event_controller.get_event, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/event/<event_id>", view_func=event_controller.get_event_detail, methods=['GET']) 
    app.add_url_rule(f"{api_prefix}/event", view_func=event_controller.post_event, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/event/<event_id>", view_func=event_controller.update_event, methods=['PUT'])
    app.add_url_rule(f"{api_prefix}/event/<event_id>", view_func=event_controller.delete_event, methods=['DELETE'])
    
    # 文件(Document)相關的路由
    app.add_url_rule(f"{api_prefix}/documents", view_func=document_controller.get_documents, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/documents/<document_id>", view_func=document_controller.get_document_detail, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/documents", view_func=document_controller.create_document, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/documents/<document_id>", view_func=document_controller.update_document, methods=['PUT'])
    app.add_url_rule(f"{api_prefix}/documents/<document_id>", view_func=document_controller.delete_document, methods=['DELETE'])
    app.add_url_rule(f"{api_prefix}/documents/<document_id>/history", view_func=document_controller.get_document_history, methods=['GET'])
    
    # 目錄(Folder)相關的路由
    app.add_url_rule(f"{api_prefix}/folders", view_func=document_controller.get_folders, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/folders", view_func=document_controller.create_folder, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/folders/<folder_id>", view_func=document_controller.update_folder, methods=['PUT'])
    app.add_url_rule(f"{api_prefix}/folders/<folder_id>", view_func=document_controller.delete_folder, methods=['DELETE'])

    # 圖片上傳與獲取
    app.add_url_rule(f"{api_prefix}/upload-image", view_func=document_controller.upload_image, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/image/<image_id>", view_func=document_controller.get_image, methods=['GET'])
    
    # certificate
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

    # Cronjob routes
    app.add_url_rule("/api/devops/cronjobs", view_func=cronjob_controller.get_cronjobs, methods=['GET'])
    app.add_url_rule("/api/devops/cronjob", view_func=cronjob_controller.add_cronjob, methods=['POST'])
    app.add_url_rule("/api/devops/cronjob/<cronjob_id>", view_func=cronjob_controller.update_cronjob, methods=['PUT'])
    app.add_url_rule("/api/devops/cronjob/<cronjob_id>", view_func=cronjob_controller.delete_cronjob, methods=['DELETE'])

    # Operation logs route
    app.add_url_rule(f"{api_prefix}/operation_logs", view_func=operation_log_controller.get_operation_logs, methods=['GET'])
    