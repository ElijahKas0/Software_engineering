import os
import json
from fastapi import UploadFile, HTTPException
from datetime import datetime, timezone
from app.database import load_data, save_data

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_file(file: UploadFile, user: dict, uploaded_by: str = None):
    uploader = uploaded_by if user["role"] == "admin" and uploaded_by else user["username"]
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    data = load_data()
    file_id = max([f["id"] for f in data.get("files", [])], default=0) + 1
    file_data = {
        "id": file_id,
        "filename": file.filename,
        "uploaded_by": uploader,
        "upload_time": datetime.now(timezone.utc).isoformat(),
    }
    data["files"].append(file_data)
    save_data(data)
    return {"message": "File uploaded successfully", "file": file_data}

async def delete_file(filename: str, user: dict):
    data = load_data()
    files = data.get("files", [])
    file_to_delete = next((f for f in files if f["filename"] == filename), None)
    
    if not file_to_delete:
        raise HTTPException(status_code=404, detail="File not found")
    
    if user["role"] != "admin" and file_to_delete["uploaded_by"] != user["username"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    data["files"] = [f for f in files if f["filename"] != filename]
    save_data(data)
    return {"message": "File deleted successfully"}