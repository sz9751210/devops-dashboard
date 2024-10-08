from flask import jsonify, request
from app.services.document_service import DocumentService
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DocumentController:
    def __init__(self, db):
        self.document_service = DocumentService(db)

    # 獲取所有文件
    def get_documents(self):
        folder_id = request.args.get('folder_id')  # 從查詢參數中獲取 folder_id
        documents = self.document_service.get_documents_by_folder(folder_id)
        return jsonify({"code": 200, "message": "success", "data": documents})

    # 獲取單一文件的詳細信息
    def get_document_detail(self, document_id):
        document = self.document_service.get_document_by_id(document_id)
        if document:
            return jsonify({"code": 200, "message": "success", "data": document})
        else:
            return jsonify({"code": 404, "message": "Document not found"}), 404

    # 新增文件
    def create_document(self):
        document_data = request.get_json()
        if not document_data:
            return jsonify({"code": 400, "message": "No input data provided"}), 400
        document_id = self.document_service.create_document(document_data)
        self.document_service.save_document_history(document_id, document_data)
        return jsonify({"code": 200, "message": "Document created successfully", "data": {"document_id": document_id}})

    # 更新文件
    def update_document(self, document_id):
        document_data = request.get_json()
        if not document_data:
            return jsonify({"code": 400, "message": "No input data provided"}), 400
        self.document_service.save_document_history(document_id, document_data)
        self.document_service.update_document(document_id, document_data)
        return jsonify({"code": 200, "message": "Document updated successfully"})

    # 刪除文件
    def delete_document(self, document_id):
        self.document_service.delete_document(document_id)
        return jsonify({"code": 200, "message": "Document deleted successfully"})

    # 獲取所有目錄
    def get_folders(self):
        folders = self.document_service.get_all_folders()
        return jsonify({"code": 200, "message": "success", "data": folders})

    # 新增目錄
    def create_folder(self):
        folder_data = request.get_json()
        if not folder_data:
            return jsonify({"code": 400, "message": "No input data provided"}), 400
        folder_id = self.document_service.create_folder(folder_data)
        return jsonify({"code": 200, "message": "Folder created successfully", "data": {"folder_id": folder_id}})

    # 更新目錄
    def update_folder(self, folder_id):
        folder_data = request.get_json()
        if not folder_data:
            return jsonify({"code": 400, "message": "No input data provided"}), 400
        self.document_service.update_folder(folder_id, folder_data)
        return jsonify({"code": 200, "message": "Folder updated successfully"})

    # 刪除目錄
    def delete_folder(self, folder_id):
        self.document_service.delete_folder(folder_id)
        return jsonify({"code": 200, "message": "Folder deleted successfully"})

    def upload_image(self):
        logger.info("Request files: %s",request.files)
        if 'file' not in request.files:
            return jsonify({"code": 400, "message": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"code": 400, "message": "No selected file"}), 400

        image_id = self.document_service.upload_image(file)
        return jsonify({"code": 200, "message": "Image uploaded successfully", "data": {"image_id": image_id}})
    
    # 獲取圖片
    def get_image(self, image_id):
        image = self.document_service.get_image(image_id)
        if image:
            return image
        else:
            return jsonify({"code": 404, "message": "Image not found"}), 404

    def get_document_history(self, document_id):
        try:
            history = self.document_service.get_document_history(document_id)
            return jsonify({"code": 200, "message": "success", "data": history})
        except Exception as e:
            logger.error(f"Error fetching document history: {e}")
            return jsonify({"code": 500, "message": "Error fetching document history"}), 500
