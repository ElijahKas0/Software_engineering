from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URL)
db = client["file_storage"]
files_collection = db["files"]

files_collection.create_index("filename")
files_collection.create_index("uploaded_by")
