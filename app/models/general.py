from pydantic import BaseModel


class GeneralFailedResponse(BaseModel):
    message: str
    errors: str
    data: None
