"""
Authentication API Router.
Endpoints for user registration and JWT login.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Dict, Any
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
                "username": user["username"],
                "name": user["name"],
                "email": user["email"]
            },
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    user = auth_service.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = create_access_token({"sub": user["id"], "username": user["username"]})
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=user["id"],
        username=user["username"],
        name=user.get("name", credentials.username.title())
    )
