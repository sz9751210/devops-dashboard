import os
from pymongo import MongoClient
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class Config:
    # MongoDB 配置
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")

    _settings_cache = None

    @staticmethod
    def get_client():
        client = MongoClient(Config.MONGO_URI)
        return client

    @classmethod
    def get_settings_from_db(cls):
        client = cls.get_client()
        db = client['it']
        collection = db['settings']
        setting = collection.find_one()
        if setting:
            return setting
        return None
    
    @classmethod
    def get_operation_logs_from_db(cls):
        client = cls.get_client()
        db = client['it']
        collection = db['operation_logs']
        return collection

    @classmethod
    def refresh_settings_cache(cls):
        cls._settings_cache = cls.get_settings_from_db()

    @classmethod
    def get_cloudflare_api_key(cls):
        if cls._settings_cache is None:
            cls.refresh_settings_cache()
        return cls._settings_cache.get('cloudflareApiKey') if cls._settings_cache else None

    @classmethod
    def get_cloudflare_email(cls):
        if cls._settings_cache is None:
            cls.refresh_settings_cache()
        return cls._settings_cache.get('cloudflareEmail') if cls._settings_cache else None

    @classmethod
    def get_telegram_bot_token(cls):
        if cls._settings_cache is None:
            cls.refresh_settings_cache()
        return cls._settings_cache.get('telegramBotToken') if cls._settings_cache else None

    @classmethod
    def get_telegram_chat_id(cls):
        if cls._settings_cache is None:
            cls.refresh_settings_cache()
        return cls._settings_cache.get('telegramChatId') if cls._settings_cache else None


def get_client():
    return Config.get_client()

def get_secret_key():
    return Config.SECRET_KEY
