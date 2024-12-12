from fastapi import Header, status
from fastapi.responses import JSONResponse
from firebase_admin import auth
from app.helpers import errors as custom_errors


def verify_token(authorization: str = Header(...)):
    try:
        if not authorization.startswith("Bearer "):
            raise custom_errors.ResponseError(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="authorization failed",
                errors="invalid authorization header",
            )

        token = authorization.split("Bearer ")[1]

        if not token:
            raise custom_errors.ResponseError(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="authorization failed",
                errors="token not found",
            )

        decoded = auth.verify_id_token(token)

        return decoded
    except auth.InvalidIdTokenError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": "authorization failed",
                "errors": "invalid token",
                "data": None,
            },
        )
    except auth.ExpiredIdTokenError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": "authorization failed",
                "errors": "expired token",
                "data": None,
            },
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "authorization failed",
                "errors": "internal server error",
                "data": None,
            },
        )
