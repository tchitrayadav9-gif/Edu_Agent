"""
Authentication API Router.
Endpoints for user registration and JWT login.
"""

from fastapi import APIRouter, HTTPException, Depends, status, Header
from pydantic import BaseModel
from typing import Dict, Any, Optional
from ..database.models import UserCreate, UserLogin, Token
from ..services.auth_service import auth_service, create_access_token


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=Dict[str, Any])
def register(user_data: UserCreate):
    try:
        user = auth_service.register_user(user_data)
        token = create_access_token({"sub": user["id"], "username": user["username"]})
        return {
            "message": "User registered successfully",
            "user": {
                "id": user["id"],
                "user_id": user["id"],
                "username": user["username"],
                "name": user["name"],
                "email": user["email"],
                "academic_year": user.get("academic_year", "2nd Year"),
                "branch": user.get("branch", "CSE")
            },
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Dict[str, Any])
def login(credentials: UserLogin):
    user = auth_service.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )
    token = create_access_token({"sub": user["id"], "username": user["username"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user["id"],
        "username": user["username"],
        "name": user.get("name", credentials.username.title()),
        "user": {
            "id": user["id"],
            "user_id": user["id"],
            "username": user["username"],
            "name": user.get("name", credentials.username.title()),
            "email": user.get("email", ""),
            "academic_year": user.get("academic_year", "2nd Year"),
            "branch": user.get("branch", "CSE")
        }
    }


@router.get("/me")
def get_current_user_profile(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token.")
    token = authorization.split(" ")[1]
    user = auth_service.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="User not found or session expired.")
    return {
        "id": user["id"],
        "user_id": user["id"],
        "username": user["username"],
        "name": user.get("name", user["username"].title()),
        "email": user.get("email", ""),
        "academic_year": user.get("academic_year", "2nd Year"),
        "branch": user.get("branch", "CSE")
    }

