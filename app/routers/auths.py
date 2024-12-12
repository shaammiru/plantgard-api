from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from firebase_admin import auth

from app.models import auths as auths_model
from app.models import general as general_model
from app.services import auths as auths_service
from app.helpers import errors as custom_errors
from app.middleware import auths as auths_middleware

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
        401: {"model": general_model.GeneralFailedResponse},
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


@router.get(
    "/profile",
    responses={
        200: {"model": auths_model.GetProfileResponse},
        400: {"model": general_model.GeneralFailedResponse},
        500: {"model": general_model.GeneralFailedResponse},
    },
    dependencies=[Depends(auths_middleware.verify_token)],
)
async def get_profile(request: Request):
    try:
        user = auth.get_user(request.state.decoded["user_id"])
        user_data = {
            "uid": user.uid,
            "email": user.email,
            "name": user.display_name,
            "phone_number": user.phone_number,
            "photo_url": user.photo_url,
            "email_verified": user.email_verified,
            "disabled": user.disabled,
        }

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "get profile success",
                "errors": None,
                "data": user_data,
            },
        )
    except custom_errors.ResponseError as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)
    except Exception as e:
        print(str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "get profile failed",
                "errors": "internal server error",
                "data": None,
            },
        )
