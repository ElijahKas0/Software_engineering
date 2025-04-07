# app/crud.py
from sqlalchemy.orm import Session
from app.models import User
from passlib.context import CryptContext
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str, full_name: str):
    existing_user = get_user_by_username(db, username)
    if existing_user:
        return {"error": "User already exists"}

    new_user = User(
        username=username,
        full_name=full_name,
        role="user",
        hashed_password=pwd_context.hash(password),
        created_at=datetime.now(timezone.utc),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
