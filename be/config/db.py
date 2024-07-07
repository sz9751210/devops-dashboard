import os
from pymongo import MongoClient

def get_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/devops")
    client = MongoClient(mongo_uri)
    db = client.get_database()
    return db
