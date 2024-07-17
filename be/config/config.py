import os
from pymongo import MongoClient
from dotenv import load_dotenv

# 加載 .env 文件中的環境變數
load_dotenv()

class Config:
    # MongoDB 配置
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    
    # Cloudflare 配置
    CLOUDFLARE_API_KEY = os.getenv('CLOUDFLARE_API_KEY')
    CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
    
    # Secret Key 配置
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")

def get_client():
    client = MongoClient(Config.MONGO_URI)
    return client

def get_secret_key():
    return Config.SECRET_KEY
