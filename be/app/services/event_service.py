from bson.objectid import ObjectId

class EventService:
    def __init__(self, client):
        db = client['it']
        self.collection = db['event']

    def get_event_list(self):
        event = list(self.collection.find({}))
        for item in event:
            item['_id'] = str(item['_id'])
        return event

    def add_event(self, event_data):
        result = self.collection.insert_one(event_data)
        return str(result.inserted_id)

    def update_event(self, event_id, event_data):
        if '_id' in event_data:
            del event_data['_id']
        self.collection.update_one(
            {'_id': ObjectId(event_id)}, {'$set': event_data})

    def delete_event(self, event_id):
        self.collection.delete_one({'_id': ObjectId(event_id)})
