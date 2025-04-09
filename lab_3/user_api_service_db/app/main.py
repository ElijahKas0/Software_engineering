# main.py
from fastapi import FastAPI
from app.routes import router
from app.init_db import init as init_db

app = FastAPI(title="Auth Service")

# Инициализация БД при старте
init_db()

# Роуты
app.include_router(router)


