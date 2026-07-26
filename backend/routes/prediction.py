from fastapi import APIRouter

import schemas
from services.prediction import predict_risk

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.post("/", response_model=schemas.PredictionResponse)
def predict(request: schemas.PredictionRequest):

    return predict_risk(request)