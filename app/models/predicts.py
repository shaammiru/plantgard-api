from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from app.models import auths


class PlantType(str, Enum):
    chili = "chili"
    corn = "corn"
    rice = "rice"


class Disease(BaseModel):
    type: str
    description: str
    treatment: str
    prevention: str


class PredictionResult(BaseModel):
    plant_type: str
    disease: Disease
    user: auths.User
    createdAt: datetime
    updatedAt: datetime


class PredictionSuccessResponse(BaseModel):
    message: str
    errors: None
    data: PredictionResult


class PredictionFailedResponse(BaseModel):
    message: str
    errors: str
    data: None


class PredictionHistoriesSuccessResponse(BaseModel):
    message: str
    errors: str
    data: list[PredictionResult]


class PredictionHistoriesFailedResponse(BaseModel):
    message: str
    errors: str
    data: None
