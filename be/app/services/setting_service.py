from bson.objectid import ObjectId

class SettingService:
    def __init__(self, client):
        db = client['it']
        self.collection = db['settings']

    
    def get_settings(self):
        settings = list(self.collection.find({}))
        for setting in settings:
            setting['_id'] = str(setting['_id'])
        return settings

    def add_setting(self, setting_data):
        result = self.collection.insert_one(setting_data)
        return str(result.inserted_id)

    def update_setting(self, setting_id, setting_data):
        setting_data['_id'] = ObjectId(setting_id)
        self.collection.update_one(
            {"_id": ObjectId(setting_id)},
            {"$set": setting_data}
        )

    def delete_setting(self, setting_id):
        self.collection.delete_one({"_id": ObjectId(setting_id)})
