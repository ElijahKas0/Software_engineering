from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer
import jwt
import os

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")

def get_current_user(token: str = Security(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        return {"username": payload["sub"], "role": payload.get("role", "user")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
