# database.py
from passlib.context import CryptContext
from datetime import datetime, timezone
import jwt
import os

# Простая "база данных" в памяти
users = {}

# Настройка для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Генерация секретного ключа
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = "HS256"

# Создание мастер-пользователя
if "admin" not in users:
    users["admin"] = {
        "username": "admin",
        "hashed_password": pwd_context.hash("secret"),
        "full_name": "Admin User",
        "role": "admin",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

def get_user(username: str):
    return users.get(username)

def create_user(username: str, password: str, full_name: str):
    if username in users:
        return {"error": "User already exists"}
    users[username] = {
        "username": username,
        "hashed_password": pwd_context.hash(password),
        "full_name": full_name,
        "role": "user",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    return {"message": "User created successfully"}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(username: str):
    payload = {"sub": username, "exp": datetime.now(timezone.utc).isoformat()}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)