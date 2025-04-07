# app/models.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
from pydantic import BaseModel

from app.database import Base

# SQLAlchemy-модель таблицы users
class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Pydantic-схемы
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str

class UserResponse(BaseModel):
    username: str
    full_name: str
    role: str

    class Config:
        orm_mode = True
