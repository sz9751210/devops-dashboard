from datetime import datetime, timedelta
import bcrypt
import jwt
from config.config import get_secret_key


class AuthService:
    def __init__(self, client):
        db = client['it']
        self.collection = db['users']
        self.secret_key = get_secret_key()

    def register_user(self, username, password):
        if self.collection.find_one({'username': username}):
            return False, '用戶名已被註冊'

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        self.collection.insert_one({
            'username': username,
            'password': hashed_password.decode('utf-8'),
            'role': 'user',
            'create_at': datetime.now()
        })
        return True, '註冊成功'

    def authenticate_user(self, username, password):
        user = self.collection.find_one({'username': username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            token = self.generate_token(user['username'])
            return True, '登入成功', token
        return False, '用戶名或密碼錯誤', None

    def generate_token(self, username):
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm='HS256'
        )
        return token
