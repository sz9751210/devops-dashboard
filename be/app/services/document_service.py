from datetime import datetime
from bson.objectid import ObjectId
from gridfs import GridFS
from pymongo import ASCENDING
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

    def save_document_history(self, document_id, document_data):
        history_collection = self.documents_collection.history
        formatted_edit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        history_data = {
            'document_id': ObjectId(document_id),
            'content': document_data.get('content'),
            'edit_time': formatted_edit_time,  # 保存編輯時間
        }
        history_collection.insert_one(history_data)

        # 檢查相同 title 的紀錄數量
        title = document_data.get('title')
        history_count = history_collection.count_documents({'title': title})

        # 如果超過 7 筆，刪除最舊的紀錄
        if history_count > 7:
            # 找到最早的紀錄，根據 edit_time 升序排序
            oldest_record = history_collection.find({'title': title}).sort('edit_time', ASCENDING).limit(1)
            # 刪除最早的紀錄
            if oldest_record:
                history_collection.delete_one({'_id': oldest_record[0]['_id']})

    def get_document_history(self, document_id, limit=7):
        history_collection = self.documents_collection.history
        history = list(history_collection.find({'document_id': ObjectId(document_id)}).sort("edit_time", -1).skip(1).limit(limit))
        logger.debug(f"get history: {history}")

        for record in history:
            # 將所有的 ObjectId 轉換為字串
            record['_id'] = str(record['_id'])
            record['document_id'] = str(record['document_id'])  # 將 document_id 也轉換成字串
            if 'folderId' in record and isinstance(record['folderId'], ObjectId):
                record['folderId'] = str(record['folderId'])  # 確保 folderId 也被轉換
        return history
