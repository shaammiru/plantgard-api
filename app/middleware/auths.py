from fastapi import Header, Request, status
from firebase_admin import auth
from app.helpers import errors as custom_errors


def verify_token(request: Request, authorization: str = Header(...)):
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
        request.state.decoded = decoded

        return decoded
    except auth.InvalidIdTokenError:
        raise custom_errors.ResponseError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="authorization failed",
            errors="invalid token",
        )
    except auth.ExpiredIdTokenError:
        raise custom_errors.ResponseError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="authorization failed",
            errors="expired token",
        )
    except Exception:
        raise custom_errors.ResponseError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="authorization failed",
            errors="internal server error",
        )
