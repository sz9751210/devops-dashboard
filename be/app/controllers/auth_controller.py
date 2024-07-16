from flask import jsonify, request
from app.services.auth_service import AuthService


class AuthController:
    def __init__(self, db):
        self.auth_service = AuthService(db)

    def register(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'code': 400, "message": '請提供用戶名和密碼'}), 400

        success, message = self.auth_service.register_user(username, password)
        if success:
            return jsonify({'code': 201, "message": '註冊成功'}), 201
        else:
            return jsonify({'code': 400, "message": message}), 400
        
    def login(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'code': 400, "message": '請提供用戶名和密碼'}), 400
        
        success, message, token= self.auth_service.authenticate_user(username, password)

        if success:
            return jsonify({'code': 200, "message": '登入成功', 'token': token}), 200
        else:
            return jsonify({'code': 400, "message": message}), 400