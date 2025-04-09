# app/crud.py
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models

# Настройка хеширования
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Получение пользователя по username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Проверка пароля
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Хеширование пароля
def hash_password(password: str):
    return pwd_context.hash(password)

# Создание пользователя
def create_user(db: Session, username: str, password: str, full_name: str):
    existing_user = get_user_by_username(db, username)
    if existing_user:
        return {"error": "User already exists"}

    hashed_pw = hash_password(password)
    db_user = models.User(
        username=username,
        hashed_password=hashed_pw,
        full_name=full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

