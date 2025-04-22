from pydantic import BaseModel
from datetime import datetime

class FileMetadata(BaseModel):
    filename: str
    uploaded_by: str
    upload_time: datetime
    file_path: str  
