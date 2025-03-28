import os
import json
from fastapi import UploadFile, HTTPException
from datetime import datetime, timezone
from app.database import load_db, save_db

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_file(file: UploadFile, user: dict, uploaded_by: str = None):
    uploader = uploaded_by if user["role"] == "admin" and uploaded_by else user["username"]

    # Создание пути для пользователя: каждая директория будет называться в честь пользователя
    user_upload_dir = os.path.join(UPLOAD_DIR, uploader)
    os.makedirs(user_upload_dir, exist_ok=True)  # Создаём директорию для пользователя, если она не существует
    
    file_path = os.path.join(user_upload_dir, file.filename)  # Путь для хранения файла пользователя
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Загрузка данных из базы данных
    data = load_db()
    file_id = max([f["id"] for f in data.get("files", [])], default=0) + 1

    # Запись информации о файле в базу данных
    file_data = {
        "id": file_id,
        "filename": file.filename,
        "uploaded_by": uploader,
        "upload_time": datetime.now(timezone.utc).isoformat(),
        # "file_path":file_path,
    }
    data["files"].append(file_data)
    save_db(data)
    
    return {"message": "File uploaded successfully", "file": file_data}

async def delete_file(filename: str, user: dict):
    data = load_db()
    files = data.get("files", [])
    file_to_delete = next((f for f in files if f["filename"] == filename), None)
    
    if not file_to_delete:
        raise HTTPException(status_code=404, detail="File not found")
    
    if user["role"] != "admin" and file_to_delete["uploaded_by"] != user["username"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    file_path = os.path.join(UPLOAD_DIR, file_to_delete["uploaded_by"], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    data["files"] = [f for f in files if f["filename"] != filename]
    save_db(data)
    return {"message": "File deleted successfully"}