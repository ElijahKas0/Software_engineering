from app.mongo.db import files_collection
from datetime import datetime
import os

def init_data():
    if files_collection.count_documents({}) == 0:
        files_collection.insert_many([
            {
                "filename": "example1.txt",
                "uploaded_by": "admin",
                "upload_time": datetime.utcnow(),
                "file_path": os.path.join("uploads", "admin", "example1.txt")
            },
            {
                "filename": "sample.jpg",
                "uploaded_by": "user123",
                "upload_time": datetime.utcnow(),
                "file_path": os.path.join("uploads", "user123", "sample.jpg")
            }
        ])
