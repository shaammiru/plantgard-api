from fastapi import APIRouter, Query, UploadFile, File, status
from fastapi.responses import JSONResponse
from datetime import datetime

from app.models import predicts as predicts_model

router = APIRouter(prefix="/predicts", tags=["Predicts"])


@router.post(
    "",
    responses={
        200: {"model": predicts_model.PredictionSuccessResponse},
        500: {"model": predicts_model.PredictionFailedResponse},
    },
)
async def predict_plant(
    plants: predicts_model.PlantType = Query(...),
    image: UploadFile = File(...),
):
    try:
        if plants == predicts_model.PlantType.chili:
            plant_type = "Chili"
        elif plants == predicts_model.PlantType.corn:
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
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "prediction success",
                "errors": None,
                "data": prediction_result,
            },
        )
    except Exception as e:
        print(str(e))

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "prediction failed",
                "errors": "internal server error",
                "data": None,
            },
        )


@router.get(
    "/histories",
    responses={
        200: {"model": predicts_model.PredictionHistoriesSuccessResponse},
        500: {"model": predicts_model.PredictionHistoriesFailedResponse},
    },
)
async def get_predict_histories():
    try:
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
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        prediction_histories = [prediction_result] * 3

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "get histories success",
                "errors": None,
                "data": prediction_histories,
            },
        )
    except Exception as e:
        print(str(e))

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "get histories failed",
                "errors": "internal server error",
                "data": None,
            },
        )
