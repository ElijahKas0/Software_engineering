# auth.py
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from app.database import get_user, verify_password, create_access_token

# Настройка схемы безопасности
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "mysecret", algorithms=["HS256"])
        user = get_user(payload["sub"])
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")