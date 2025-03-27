from pydantic import BaseModel
from datetime import datetime

class FileDocument(BaseModel):
    id: int
    filename: str
    uploaded_by: str
    upload_time: datetime
