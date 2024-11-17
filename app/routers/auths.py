from fastapi import APIRouter

router = APIRouter(prefix="/auths", tags=["Auths"])


@router.post("/register")
async def predict_chili():
    return {"message": "OK", "errors": None, "data": "register success"}


@router.post("/login")
async def predict_corn():
    return {"message": "OK", "errors": None, "data": "login success"}
