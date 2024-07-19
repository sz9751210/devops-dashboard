from flask import jsonify, request
from app.services.setting_service import SettingService

class SettingController:
    def __init__(self, db):
        self.setting_service = SettingService(db)

    def get_settings(self):
        settings = self.setting_service.get_settings()
        return jsonify({"code": 200, "message": "success", "data": settings})

    def add_setting(self):
        setting_data = request.get_json()
        if not setting_data:
            return jsonify({"code": 400, "message": "No input data provided"}), 400
        setting_id = self.setting_service.add_setting(setting_data)
        return jsonify({"code": 200, "message": "Settings saved successfully", "data": {"setting_id": setting_id}})
    
    def update_setting(self, setting_id):
        setting_data = request.get_json()
        self.setting_service.update_setting(setting_id, setting_data)
        return jsonify({"code": 200, "message": "Setting updated successfully"})

    def delete_setting(self, setting_id):
        self.setting_service.delete_setting(setting_id)
        return jsonify({"code": 200, "message": "Setting deleted successfully"})
