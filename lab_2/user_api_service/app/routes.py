from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import get_current_user
from app.database import get_user, create_user, verify_password, create_access_token
from app.models import UserCreate, UserResponse

router = APIRouter()

@router.post("/token", tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Эндпоинт для аутентификации пользователя и выдачи JWT-токена"""
    user = get_user(form_data.username)  # Получаем пользователя из базы

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(user["username"])
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=UserResponse, tags=["Users"])
async def register(user: UserCreate):
    """Эндпоинт для регистрации нового пользователя"""
    result = create_user(user.username, user.password, user.full_name)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return UserResponse(username=user.username, full_name=user.full_name, role="user")

@router.get("/users/me", response_model=UserResponse, tags=["Users"])
async def get_me(user: dict = Depends(get_current_user)):
    """Эндпоинт для получения информации о текущем пользователе"""
    return UserResponse(username=user["username"], full_name=user["full_name"], role=user["role"])
