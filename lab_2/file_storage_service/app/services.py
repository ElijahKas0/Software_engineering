import os
import json
from fastapi import UploadFile
from datetime import datetime, timezone
from app.database import load_data, save_data

UPLOAD_DIR = "uploads"
DB_FILE = "file_data.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_file(file: UploadFile, user: dict):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    data = load_data()
    file_id = max([f["id"] for f in data], default=0) + 1
    file_data = {
        "id": file_id,
        "filename": file.filename,
        "uploaded_by": user["username"],
        "upload_time": datetime.now(timezone.utc).isoformat(),
    }
    data.append(file_data)
    save_data(data)
    return {"message": "File uploaded successfully", "file": file_data}

async def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return {"message": "File found", "filename": filename}

async def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        data = load_data()
        data = [f for f in data if f["filename"] != filename]
        save_data(data)
        return {"message": "File deleted successfully"}
    return {"error": "File not found"}