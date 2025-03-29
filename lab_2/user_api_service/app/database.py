import json
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

# Файл для хранения пользователей
DB_FILE = "USER_DB.json"

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Секретный ключ для JWT
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = "HS256"

# Функция загрузки базы данных
def load_db():
    """Загружает пользователей из JSON-файла."""
    if not os.path.exists(DB_FILE):
        return {"users": {}}
    with open(DB_FILE, "r") as f:
        return json.load(f)

# Функция сохранения базы данных
def save_db(data):
    """Сохраняет пользователей в JSON-файл."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Проверяем, есть ли уже база, если нет – создаем с админом
db = load_db()
if "admin" not in db["users"]:
    db["users"]["admin"] = {
        "username": "admin",
        "hashed_password": pwd_context.hash("secret"),
        "full_name": "Admin User",
        "role": "admin",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    save_db(db)  # Сохранение изменений

# Функция получения пользователя
def get_user(username: str):
    """Получает пользователя по имени."""
    db = load_db()
    return db["users"].get(username)

# Функция создания нового пользователя
def create_user(username: str, password: str, full_name: str):
    """Создаёт нового пользователя и сохраняет в базу данных."""
    db = load_db()
    if username in db["users"]:
        return {"error": "User already exists"}

    db["users"][username] = {
        "username": username,
        "hashed_password": pwd_context.hash(password),
        "full_name": full_name,
        "role": "user",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    save_db(db)
    return {"message": "User created successfully"}

# Функция проверки пароля
def verify_password(plain_password, hashed_password):
    """Проверяет соответствие пароля его хешу."""
    return pwd_context.verify(plain_password, hashed_password)

# Функция создания токена доступа
def create_access_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {"sub": username, "exp": int(expire.timestamp())}  # ✅ Правильный формат
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
