# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import authenticate_user, get_current_user
from app.database import create_user, create_access_token
from app.models import UserCreate, UserResponse
from app.routes import router

app = FastAPI(title="Auth Service")

app.include_router(router)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(user["username"])
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=UserResponse)
async def register(user: UserCreate):
    result = create_user(user.username, user.password, user.full_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return UserResponse(username=user.username, full_name=user.full_name, role="user")

@app.get("/users/me", response_model=UserResponse)
async def get_me(user: dict = Depends(get_current_user)):
    return UserResponse(username=user["username"], full_name=user["full_name"], role=user["role"])
