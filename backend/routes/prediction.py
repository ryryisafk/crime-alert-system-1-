from fastapi import APIRouter, HTTPException

import schemas
from services.prediction import predict_risk

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.post("/", response_model=schemas.PredictionResponse)
def predict(request: schemas.PredictionRequest):
    risk, confidence = predict_risk(request.district, request.crime_type)

    if risk is None:
        raise HTTPException(
            status_code=400,
            detail="Unknown district or crime_type — not seen during training"
        )

    return {"predicted_risk": risk, "confidence": confidence}