from flask import jsonify
from app.services.operation_log_service import OperationLogService

class OperationLogController:
    def __init__(self, db):
        self.operation_log_service = OperationLogService(db)

    def get_operation_logs(self):
        logs = self.operation_log_service.get_operation_logs()
        return jsonify({"code": 200, "message": "success", "data": logs, "total": len(logs)})