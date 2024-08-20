from bson.objectid import ObjectId

class DocumentService:
    def __init__(self, client):
        db = client['it']
        self.documents_collection = db['documents']
        self.folders_collection = db['folders']

    # 文件操作
    def get_all_documents(self):
        documents = list(self.documents_collection.find({}, {"title": 1, "author": 1, "date": 1, "folderId": 1}))
        for document in documents:
            document['_id'] = str(document['_id'])
        return documents

    # 根據 folder_id 過濾文件，如果沒有提供 folder_id，則返回所有文件
    def get_documents_by_folder(self, folder_id=None):
        query = {}
        if folder_id:
            query['folderId'] = folder_id

        documents = list(self.documents_collection.find(query, {"title": 1, "author": 1, "date": 1, "folderId": 1}))
        for document in documents:
            document['_id'] = str(document['_id'])
        return documents

    def get_document_by_id(self, document_id):
        document = self.documents_collection.find_one({'_id': ObjectId(document_id)})
        if document:
            document['_id'] = str(document['_id'])
        return document

    def create_document(self, document_data):
        result = self.documents_collection.insert_one(document_data)
        return str(result.inserted_id)

    def update_document(self, document_id, document_data):
        if '_id' in document_data:
            del document_data['_id']
        self.documents_collection.update_one(
            {'_id': ObjectId(document_id)}, {'$set': document_data})

    def delete_document(self, document_id):
        self.documents_collection.delete_one({'_id': ObjectId(document_id)})

    # 目錄操作
    def get_all_folders(self):
        folders = list(self.folders_collection.find({}))
        for folder in folders:
            folder['_id'] = str(folder['_id'])
        return folders

    def create_folder(self, folder_data):
        result = self.folders_collection.insert_one(folder_data)
        return str(result.inserted_id)

    def update_folder(self, folder_id, folder_data):
        if '_id' in folder_data:
            del folder_data['_id']
        self.folders_collection.update_one(
            {'_id': ObjectId(folder_id)}, {'$set': folder_data})

    def delete_folder(self, folder_id):
        self.folders_collection.delete_one({'_id': ObjectId(folder_id)})
