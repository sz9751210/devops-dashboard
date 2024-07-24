class OperationLogService:
    def __init__(self, client):
        db = client['it']
        self.collection = db['operation_logs']
        self.create_ttl_index()

    def create_ttl_index(self):
        # 設定 TTL 索引，保留30天的日志
        self.collection.create_index("timestamp", expireAfterSeconds=30*24*60*60)

    def get_operation_logs(self):
        logs = list(self.collection.find())
        for log in logs:
            log['_id'] = str(log['_id'])
        return logs
