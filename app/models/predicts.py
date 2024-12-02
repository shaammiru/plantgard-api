from pydantic import BaseModel
from datetime import datetime
from typing import Optional
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


class PredictionResponse(BaseModel):
    message: str
    errors: Optional[str]
    data: PredictionResult


class PredictionHistoriesResponse(BaseModel):
    message: str
    errors: Optional[str]
    data: list[PredictionResult]
