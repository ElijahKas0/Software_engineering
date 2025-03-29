# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import authenticate_user, get_current_user
from app.database import create_user, create_access_token
from app.models import UserCreate, UserResponse
from app.routes import router

app = FastAPI(title="Auth Service")

app.include_router(router)

