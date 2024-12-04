from fastapi import HTTPException


class ResponseError(HTTPException):
    def __init__(self, status_code: int, message: str, errors: str):
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "errors": errors,
                "data": None,
            },
        )
