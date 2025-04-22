from app.mongo.db import files_collection
from datetime import datetime

def create_file_record(filename: str, uploaded_by: str, file_path: str):
    file_data = {
        "filename": filename,
        "uploaded_by": uploaded_by,
        "upload_time": datetime.utcnow(),
        "file_path": file_path
    }
    result = files_collection.insert_one(file_data)
    return str(result.inserted_id)

def get_all_files():
    return list(files_collection.find({}, {"_id": 0}))

def get_file_by_name(filename: str):
    return files_collection.find_one({"filename": filename}, {"_id": 0})

def delete_file_record(filename: str):
    return files_collection.delete_one({"filename": filename}).deleted_count
