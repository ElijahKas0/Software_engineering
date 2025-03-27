from fastapi import FastAPI, Depends, UploadFile, File, Query
from app.auth import get_current_user
from app.services import upload_file, delete_file

app = FastAPI(title="File Service API")

@app.post("/files/upload")
async def upload(
    file: UploadFile = File(...), 
    user: dict = Depends(get_current_user),
    uploaded_by: str = Query(None, description="Username of the file owner (admin only)")
):
    return await upload_file(file, user, uploaded_by)

# @app.get("/files/{filename}")
# async def get_file_route(filename: str, user: dict = Depends(get_current_user)):
#     # return await get_file(filename)

@app.delete("/files/{filename}")
async def delete_file_route(filename: str, user: dict = Depends(get_current_user)):
    return await delete_file(filename, user)
