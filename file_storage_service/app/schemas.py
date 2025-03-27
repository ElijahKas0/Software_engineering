from pydantic import BaseModel
from datetime import datetime

class FileMetadata(BaseModel):
    id: int
    filename: str
    uploaded_by: str
    upload_time: datetime
