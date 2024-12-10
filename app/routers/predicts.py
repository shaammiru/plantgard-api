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
    """
    Endpoint untuk memprediksi penyakit tanaman berdasarkan jenis tanaman dan gambar yang diunggah.
    """
    try:
        # Validasi tipe tanaman
        if plants not in [predicts_model.PlantType.chili, predicts_model.PlantType.corn, predicts_model.PlantType.rice]:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Invalid plant type",
                    "errors": "plant_validation_error",
                    "data": None,
                },
            )

        # Validasi tipe file
        if image.content_type not in ["image/jpeg", "image/png"]:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Invalid file type. Only JPEG and PNG are allowed.",
                    "errors": "file_validation_error",
                    "data": None,
                },
            )

        # Tentukan jenis tanaman
        plant_type = plants.value.capitalize()

        # Mock hasil prediksi
        prediction_result = {
            "plant_type": plant_type,
            "disease": {
                "type": "Example Disease",
                "description": "Example disease is a bla bla bla.",
                "treatment": "Disease treatment.",
                "prevention": "Disease prevention.",
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
        # Tangani error tidak terduga
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Prediction failed",
                "errors": str(e),
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
    """
    Endpoint untuk mendapatkan histori prediksi penyakit tanaman.
    """
    try:
        # Mock data histori
        prediction_result = {
            "plant_type": "Chili",
            "disease": {
                "type": "Example Disease",
                "description": "Example disease is a bla bla bla.",
                "treatment": "Disease treatment.",
                "prevention": "Disease prevention.",
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
        # Tangani error tidak terduga
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "get histories failed",
                "errors": str(e),
                "data": None,
            },
        )
