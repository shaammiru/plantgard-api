from fastapi import APIRouter

router = APIRouter(prefix="/predicts", tags=["Predicts"])


@router.post("/chili")
async def predict_chili():
    return {"message": "OK", "errors": None, "data": "chili prediction result"}


@router.post("/corn")
async def predict_corn():
    return {"message": "OK", "errors": None, "data": "corn prediction result"}


@router.post("/rice")
async def predict_rice():
    return {"message": "OK", "errors": None, "data": "rice prediction result"}
