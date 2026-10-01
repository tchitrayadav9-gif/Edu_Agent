"""
Authentication Service.
Manages user registration, password hashing with passlib/hash, and JWT token issuance/validation.
"""

import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from ..database.mongodb import db_manager
from ..database.models import UserCreate, User

SECRET_KEY = os.getenv("JWT_SECRET", "edumind_development_secret_key_884920482018")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))


def hash_password(password: str) -> str:
    """Deterministic hash with salt."""
    salt = "edumind_salt_2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


class AuthService:
    """User authentication and credential verification."""
    
    def __init__(self):
        self.db = db_manager

    def register_user(self, user_in: UserCreate) -> Dict[str, Any]:
        """Register a new student user."""
        existing = self.db.users.find_one({"username": user_in.username})
        if existing:
            raise ValueError(f"Username '{user_in.username}' already registered.")
        
        user_record = {
            "id": f"user_{user_in.username.lower()}",
            "username": user_in.username,
            "email": user_in.email,
            "name": user_in.name,
            "academic_year": user_in.academic_year or "2nd Year",
            "branch": user_in.branch or "Computer Science and Engineering",
            "password_hash": hash_password(user_in.password),
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }
        self.db.users.insert_one(user_record)

        # Initialize default student profile
        from .student_service import student_service
        student_service.get_or_create_profile(user_record["id"], default_name=user_in.name)

        return user_record

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Verify username & password."""
        user = self.db.users.find_one({"username": username})
        if not user:
            # Auto-create demo user for smooth first-time demo if 'demo' or 'chitra'
            if username.lower() in ["chitra", "demo", "student"]:
                user = self.register_user(UserCreate(
                    username=username,
                    email=f"{username}@eduagent.ai",
                    name=username.title(),
                    password=password
                ))
            else:
                return None
        
        if verify_password(password, user.get("password_hash", "")):
            return user
        return None


# Global auth service instance
auth_service = AuthService()
