from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from firebase_admin import auth

from app.models import auths as auths_model
from app.models import general as general_model
from app.services import auths as auths_service
from app.helpers import errors as custom_errors

router = APIRouter(prefix="/auths", tags=["Auths"])


@router.post(
    "/register",
    responses={
        201: {"model": auths_model.RegisterSuccessResponse},
        400: {"model": general_model.GeneralFailedResponse},
        500: {"model": general_model.GeneralFailedResponse},
    },
)
async def register(request: auths_model.RegisterRequest):
    try:
        response = auths_service.register_user(request)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)
    except auth.EmailAlreadyExistsError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "register failed",
                "errors": "email is already registered",
                "data": None,
            },
        )
    except Exception as e:
        print(str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "register failed",
                "errors": "internal server error",
                "data": None,
            },
        )


@router.post(
    "/login",
    responses={
        200: {"model": auths_model.LoginSuccessResponse},
        400: {"model": general_model.GeneralFailedResponse},
        500: {"model": general_model.GeneralFailedResponse},
    },
)
async def login(request: auths_model.LoginRequest):
    try:
        response = auths_service.login_user(request)
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)
    except custom_errors.ResponseError as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)
    except Exception as e:
        print(str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "login failed",
                "errors": "internal server error",
                "data": None,
            },
        )


@router.post(
    "/refresh-token",
    responses={
        200: {"model": auths_model.RefreshResponse},
        400: {"model": general_model.GeneralFailedResponse},
        500: {"model": general_model.GeneralFailedResponse},
    },
)
async def refresh_token(request: auths_model.RefreshRequest):
    try:
        response = auths_service.exchange_refresh_token(request)
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)
    except custom_errors.ResponseError as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)
    except Exception as e:
        print(str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "exchange token failed",
                "errors": "internal server error",
                "data": None,
            },
        )
