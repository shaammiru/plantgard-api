import os
import requests
from fastapi import status
from firebase_admin import auth
from app.models import auths as auths_model
from app.helpers import errors as custom_errors


def register_user(request: auths_model.RegisterRequest):
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


def login_user(request: auths_model.LoginRequest):
    firebase_api_key = os.getenv("FIREBASE_API_KEY")
    if not firebase_api_key:
        raise Exception

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"

    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True,
    }

    response = requests.post(url, json=payload)
    response_data = response.json()

    if response.status_code != 200:
        error_message = response_data.get("error", {}).get("message", "login failed")

        match error_message:
            case "INVALID_LOGIN_CREDENTIALS":
                raise custom_errors.ResponseError(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="login failed",
                    errors="invalid email or password",
                )

            case _:
                raise custom_errors.ResponseError(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="login failed",
                    errors="client unknown error",
                )

    return {
        "message": "login success",
        "errors": None,
        "data": {
            "token": response_data["idToken"],
            "refresh_token": response_data["refreshToken"],
        },
    }


def exchange_refresh_token(request: auths_model.RefreshRequest):
    firebase_api_key = os.getenv("FIREBASE_API_KEY")
    if not firebase_api_key:
        raise Exception

    url = f"https://securetoken.googleapis.com/v1/token?key={firebase_api_key}"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token,
    }

    response = requests.post(url, data=payload)

    response_data = response.json()

    if response.status_code != 200:
        error_message = response_data.get("error", {}).get(
            "message", "exchange token failed"
        )

        match error_message:
            case "INVALID_REFRESH_TOKEN":
                raise custom_errors.ResponseError(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="exchange token failed",
                    errors="invalid refresh token",
                )

            case _:
                raise Exception

    return {
        "message": "exchange token success",
        "errors": None,
        "data": {
            "token": response_data["id_token"],
            "refresh_token": response_data["refresh_token"],
        },
    }
