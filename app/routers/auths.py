import os
import requests
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from firebase_admin import auth

from app.models import auths as auths_model

router = APIRouter(prefix="/auths", tags=["Auths"])


@router.post(
    "/register",
    responses={
        201: {"model": auths_model.RegisterSuccessResponse},
        400: {"model": auths_model.RegisterFailedResponse},
        500: {"model": auths_model.RegisterFailedResponse},
    },
)
async def register(request: auths_model.RegisterRequest):
    try:
        user = auth.create_user(
            email=request.email,
            password=request.password,
            display_name=request.name,
        )

        return {
            "message": "register success",
            "errors": None,
            "data": {
                "user": {
                    "uid": user.uid,
                    "name": user.display_name,
                    "email": user.email,
                }
            },
        }
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
        400: {"model": auths_model.LoginFailedResponse},
        500: {"model": auths_model.LoginFailedResponse},
    },
)
async def login(request: auths_model.LoginRequest):
    try:
        firebase_api_key = os.getenv("FIREBASE_API_KEY")
        if not firebase_api_key:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": "login failed",
                    "errors": "firebase api key not set",
                    "data": None,
                },
            )

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"

        payload = {
            "email": request.email,
            "password": request.password,
            "returnSecureToken": True,
        }

        response = requests.post(url, json=payload)
        response_data = response.json()

        if response.status_code != 200:
            error_message = response_data.get("error", {}).get(
                "message", "login failed"
            )

            match error_message:
                case "INVALID_LOGIN_CREDENTIALS":
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={
                            "message": "login failed",
                            "errors": "invalid email or password",
                            "data": None,
                        },
                    )
                case _:
                    print(error_message)

                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={
                            "message": "login failed",
                            "errors": "client unknown error",
                            "data": None,
                        },
                    )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "login success",
                "errors": None,
                "data": {"token": response_data["idToken"]},
            },
        )
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
