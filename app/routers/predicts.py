from fastapi import APIRouter, Query, Depends, Request, UploadFile, File, status
from fastapi.responses import JSONResponse

from app.models import predicts as predicts_model
from app.services import predicts as predicts_service
from app.middleware import auths as auths_middleware
from app.helpers import errors as custom_errors, firebase

router = APIRouter(prefix="/predicts", tags=["Predicts"])


@router.post(
    "",
    responses={
        200: {"model": predicts_model.PredictionSuccessResponse},
        500: {"model": predicts_model.PredictionFailedResponse},
    },
    dependencies=[Depends(auths_middleware.verify_token)],
)
async def predict_plant(
    request: Request,
    plants: predicts_model.PlantType = Query(...),
    image: UploadFile = File(...),
):
    try:
        user = {
            "uid": request.state.decoded["user_id"],
            "name": request.state.decoded["name"],
            "email": request.state.decoded["email"],
        }

        if plants not in [
            predicts_model.PlantType.chili,
            predicts_model.PlantType.corn,
            predicts_model.PlantType.rice,
        ]:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "invalid plant type",
                    "errors": "plant_validation_error",
                    "data": None,
                },
            )

        if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "invalid file type. Only JPEG and PNG are allowed.",
                    "errors": "file_validation_error",
                    "data": None,
                },
            )

        prediction_result = predicts_service.predict_image(plants, image, user)
        firebase.db.collection("predictions").add(prediction_result)

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
    dependencies=[Depends(auths_middleware.verify_token)],
)
async def get_predict_histories(request: Request):
    try:
        prediction_ref = firebase.db.collection("predictions")
        query = prediction_ref.where("user.uid", "==", request.state.decoded["user_id"])
        prediction_stream = query.stream()

        prediction_histories = []
        for prediction in prediction_stream:
            prediction_histories.append(prediction.to_dict())

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "get histories success",
                "errors": None,
                "data": prediction_histories,
            },
        )
    except custom_errors.ResponseError as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)
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
