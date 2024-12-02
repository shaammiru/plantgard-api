from fastapi import APIRouter, Query, UploadFile, File
from datetime import datetime

from app.models import predicts

router = APIRouter(prefix="/predicts", tags=["Predicts"])


@router.post("", response_model=predicts.PredictionResponse)
async def predict_plant(
    plants: predicts.PlantType = Query(...),
    image: UploadFile = File(...),
):
    if plants == predicts.PlantType.chili:
        plant_type = "Chili"
    elif plants == predicts.PlantType.corn:
        plant_type = "Corn"
    else:
        plant_type = "Rice"

    prediction_result = {
        "plant_type": plant_type,
        "disease": {
            "type": "Example Disease",
            "description": "Example disease is a bla bla bla.",
            "treatment": "Disesase treatment.",
            "prevention": "Disesase prevention.",
        },
        "user": {
            "uid": "example uid",
            "name": "John Doe",
            "email": "john.doe@example.com",
        },
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
    }

    return {
        "message": "prediction success",
        "errors": None,
        "data": prediction_result,
    }


@router.get("/histories", response_model=predicts.PredictionHistoriesResponse)
async def get_predict_histories():
    prediction_result = {
        "plant_type": "Chili",
        "disease": {
            "type": "Example Disease",
            "description": "Example disease is a bla bla bla.",
            "treatment": "Disesase treatment.",
            "prevention": "Disesase prevention.",
        },
        "user": {
            "uid": "example uid",
            "name": "John Doe",
            "email": "john.doe@example.com",
        },
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
    }

    prediction_histories = [prediction_result] * 3

    return {
        "message": "prediction histories",
        "errors": None,
        "data": prediction_histories,
    }
