# app/init_db.py
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import User
from passlib.context import CryptContext
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "admin").first()
        if not user:
            admin = User(
                username="admin",
                full_name="Admin User",
                role="admin",
                hashed_password=pwd_context.hash("secret"),
                created_at=datetime.now(timezone.utc),
            )
            db.add(admin)
            db.commit()
            print("[init_db] ✅ Admin user created")
        else:
            print("[init_db] 🔄 Admin user already exists")
    finally:
        db.close()
