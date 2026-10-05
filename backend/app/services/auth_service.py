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
        """Register a new student user and create persistent profile in database."""
        clean_username = user_in.username.strip()
        clean_email = user_in.email.strip().lower()
        clean_password = user_in.password.strip()

        # Check existing username or email in database
        all_u = self.db.users.find()
        for u in all_u:
            if u.get("username", "").lower() == clean_username.lower():
                raise ValueError(f"Username '{clean_username}' is already taken.")
            if u.get("email", "").lower() == clean_email.lower():
                raise ValueError(f"Email '{clean_email}' is already registered.")

        user_id = f"user_{clean_username.lower().replace(' ', '_')}"
        user_record = {
            "id": user_id,
            "user_id": user_id,
            "username": clean_username,
            "email": clean_email,
            "name": user_in.name.strip(),
            "academic_year": user_in.academic_year or "2nd Year",
            "branch": user_in.branch or "Computer Science and Engineering",
            "password_hash": hash_password(clean_password),
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }
        # Save user record permanently in MongoDB Atlas users collection
        self.db.users.update_one({"username": clean_username}, {"$set": user_record}, upsert=True)

        # Initialize student profile with declared career goal and skills
        from .student_service import student_service
        profile_data = {
            "user_id": user_id,
            "name": user_in.name.strip(),
            "academic_year": user_in.academic_year or "2nd Year",
            "branch": user_in.branch or "Computer Science and Engineering",
            "career_goal": user_in.career_goal or "AI Engineer",
            "target_role": user_in.career_goal or "AI Engineer"
        }
        if user_in.skills:
            profile_data["skills"] = user_in.skills
        student_service.update_profile(user_id, profile_data)

        # Store initial career goal memory
        from ..memory.long_term_memory import long_term_memory
        long_term_memory.save_memory(
            user_id=user_id,
            memory_type="career_goal",
            content=f"Target Career Goal is {user_in.career_goal or 'AI Engineer'}.",
            importance=1.0,
            source="user_registration",
            metadata={"career_goal": user_in.career_goal or "AI Engineer"}
        )

        return user_record

    def authenticate_user(self, username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
        """Verify credentials by username or email from MongoDB cluster."""
        clean_input = username_or_email.strip()
        clean_pass = password.strip()
        
        # Search by username or email
        user = self.db.users.find_one({"username": clean_input})
        if not user:
            user = self.db.users.find_one({"email": clean_input.lower()})

        if not user:
            # Check case-insensitive across collection
            all_u = self.db.users.find()
            for u in all_u:
                if u.get("username", "").lower() == clean_input.lower() or u.get("email", "").lower() == clean_input.lower():
                    user = u
                    break

        if not user:
            # Auto-create demo user for smooth first-time demo if 'demo' or 'chitra'
            if clean_input.lower() in ["chitra", "demo", "student"]:
                try:
                    user = self.register_user(UserCreate(
                        username=clean_input.lower(),
                        email=f"{clean_input.lower()}@eduagent.ai",
                        name=clean_input.title(),
                        password=clean_pass,
                        career_goal="AI Engineer"
                    ))
                except Exception:
                    user = self.db.users.find_one({"username": clean_input.lower()})
            else:
                return None

        if not user:
            return None

        # Verify password hash
        if verify_password(clean_pass, user.get("password_hash", "")):
            return user

        # Support fallback password variants for standard demo user 'chitra'
        if user.get("username", "").lower() == "chitra" and clean_pass.lower() in ["chitra", "chitra123", "chitra@123", "admin"]:
            # Update hash with latest verified password
            new_hash = hash_password(clean_pass)
            self.db.users.update_one({"_id": user["_id"]}, {"$set": {"password_hash": new_hash}})
            user["password_hash"] = new_hash
            return user

        return None

    def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user record from JWT token payload."""
        payload = decode_token(token)
        if not payload:
            return None
        user_id = payload.get("sub")
        return self.db.users.find_one({"id": user_id})



# Global auth service instance
auth_service = AuthService()
