"""
Authentication request / response schemas.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.user import UserRole


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: "UserOut"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    type: Optional[str] = None
    exp: Optional[int] = None


# Forward reference fix
from app.schemas.user import UserOut
TokenResponse.model_rebuild()
