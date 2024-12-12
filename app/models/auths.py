from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    uid: str
    name: str
    email: EmailStr


class FullUser(BaseModel):
    uid: str
    email: EmailStr
    name: str
    phone_number: str | None
    photo_url: str | None
    email_verified: bool
    disabled: bool


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


class RefreshRequest(BaseModel):
    refresh_token: str


class RegisterData(BaseModel):
    user: User


class RegisterSuccessResponse(BaseModel):
    message: str
    errors: None
    data: RegisterData


class LoginData(BaseModel):
    token: str
    refesh_token: str


class LoginSuccessResponse(BaseModel):
    message: str
    errors: None
    data: LoginData


class RefreshResponse(BaseModel):
    message: str
    errors: None
    data: LoginData


class GetProfileData(BaseModel):
    user: FullUser


class GetProfileResponse(BaseModel):
    message: str
    errors: None
    data: GetProfileData
