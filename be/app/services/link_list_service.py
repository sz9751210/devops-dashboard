class LinkListService:
    def __init__(self, db):
        self.collection = db['link_list']

    def get_link_list(self):
        link_list = list(self.collection.find({}))
        for item in link_list:
            item['_id'] = str(item['_id'])
        return link_list
