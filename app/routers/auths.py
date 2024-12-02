from fastapi import APIRouter

from app.models import auths

router = APIRouter(prefix="/auths", tags=["Auths"])


@router.post("/register", response_model=auths.RegisterResponse)
async def register(request: auths.RegisterRequest):
    return {
        "message": "register success",
        "errors": None,
        "data": {
            "user": {
                "uid": "string",
                "name": "John Doe",
                "email": "john.doe@example.com",
            }
        },
    }


@router.post("/login", response_model=auths.LoginResponse)
async def login(request: auths.LoginRequest):
    return {
        "message": "login success",
        "errors": None,
        "data": {"token": "example token"},
    }
