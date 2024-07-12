import os
from pymongo import MongoClient

def get_client():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    return client
