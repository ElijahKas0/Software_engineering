from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_user_by_username, create_user, verify_password
from app.models import UserCreate, UserResponse
from app.auth import create_access_token, get_current_user

router = APIRouter()

@router.post("/token", tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/users/", response_model=UserResponse, tags=["Users"])
async def register(user: UserCreate, db: Session = Depends(get_db)):
    result = create_user(db, user.username, user.password, user.full_name)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return UserResponse(username=result.username, full_name=result.full_name, role=result.role)

@router.get("/users/me", response_model=UserResponse, tags=["Users"])
async def get_me(user = Depends(get_current_user)):
    return user  

