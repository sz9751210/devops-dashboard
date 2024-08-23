from bson.objectid import ObjectId
from gridfs import GridFS
from flask import jsonify, send_file
import io
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self, client):
        db = client['it']
        self.documents_collection = db['documents']
        self.folders_collection = db['folders']
        self.fs = GridFS(db)

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

    # 上傳圖片
    def upload_image(self, image_file):
        image_id = self.fs.put(image_file, filename=image_file.filename)
        return str(image_id)

    # 獲取圖片
    def get_image(self, image_id):
        try:
            # 記錄下收到的 image_id
            logger.debug(f"Attempting to retrieve image with ID: {image_id}")
            
            # 嘗試從 GridFS 中獲取圖片
            image = self.fs.get(ObjectId(image_id))
            
            # 如果成功獲取圖片，記錄圖片的部分信息
            logger.debug(f"Image retrieved: {image.filename}, {image.length} bytes")
            
            mimetype = image.content_type if image.content_type else 'application/octet-stream'
            
            return send_file(io.BytesIO(image.read()), mimetype=mimetype, download_name=image.filename)
        except Exception as e:
            # 如果發生錯誤，記錄下錯誤信息
            logger.error(f"Error retrieving image: {e}")
            return jsonify({"code": 404, "message": "Image not found"}), 404
