from flask import jsonify, request
from app.services.cronjob_service import CronjobService

class CronjobController:
    def __init__(self, client, scheduler):
        self.cronjob_service = CronjobService(client, scheduler)

    def get_cronjobs(self):
        cronjobs = self.cronjob_service.get_cronjobs()
        for cronjob in cronjobs:
            cronjob['_id'] = str(cronjob['_id'])
        return jsonify({"code": 200, "message": "success", "data": cronjobs})

    def add_cronjob(self):
        cronjob_data = request.get_json()
        cronjob_id = self.cronjob_service.add_cronjob(cronjob_data)
        return jsonify({"code": 200, "message": "Cronjob 已保存", "data": {"cronjob_id": cronjob_id}})

    def update_cronjob(self, cronjob_id):
        cronjob_data = request.get_json()
        self.cronjob_service.update_cronjob(cronjob_id, cronjob_data)
        return jsonify({"code": 200, "message": "Cronjob 更新成功"})

    def delete_cronjob(self, cronjob_id):
        self.cronjob_service.delete_cronjob(cronjob_id)
        return jsonify({"code": 200, "message": "Cronjob 已刪除"})
