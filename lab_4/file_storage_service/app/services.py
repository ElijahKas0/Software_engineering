import os
from fastapi import UploadFile, HTTPException
from datetime import datetime, timezone
from app.mongo.crud import create_file_record, get_file_by_name, delete_file_record

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_file(file: UploadFile, user: dict, uploaded_by: str = None):
    uploader = uploaded_by if user["role"] == "admin" and uploaded_by else user["username"]

    user_upload_dir = os.path.join(UPLOAD_DIR, uploader)
    os.makedirs(user_upload_dir, exist_ok=True)

    file_path = os.path.join(user_upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    create_file_record(file.filename, uploader, file_path)

    return {
        "message": "File uploaded successfully",
        "file": {
            "filename": file.filename,
            "uploaded_by": uploader,
            "upload_time": datetime.now(timezone.utc).isoformat(),
            "file_path": file_path
        }
    }

async def delete_file(filename: str, user: dict):
    file_info = get_file_by_name(filename)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")

    if user["role"] != "admin" and file_info["uploaded_by"] != user["username"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    file_path = file_info.get("file_path")
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    deleted_count = delete_file_record(filename)
    if deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete from DB")

    return {"message": "File deleted successfully"}
