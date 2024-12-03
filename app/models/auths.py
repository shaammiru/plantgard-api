from pydantic import BaseModel, EmailStr, Field


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


class RegisterData(BaseModel):
    user: User


class RegisterSuccessResponse(BaseModel):
    message: str
    errors: None
    data: RegisterData


class RegisterFailedResponse(BaseModel):
    message: str
    errors: str
    data: None


class LoginData(BaseModel):
    token: str


class LoginSuccessResponse(BaseModel):
    message: str
    errors: None
    data: LoginData


class LoginFailedResponse(BaseModel):
    message: str
    errors: str
    data: None
