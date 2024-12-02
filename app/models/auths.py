from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    uid: str
    name: str
    email: EmailStr


class RegisterRequest(BaseModel):
    name: str = Field(..., description="User's full name")
    email: EmailStr
    password: str = Field(
        ..., min_length=8, description="Password with at least 8 characters"
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        ..., min_length=8, description="Password with at least 8 characters"
    )


class RegisterResponse(BaseModel):
    message: str
    errors: Optional[str] = None
    data: User


class Token(BaseModel):
    token: str


class LoginResponse(BaseModel):
    message: str
    errors: Optional[str] = None
    data: Token
