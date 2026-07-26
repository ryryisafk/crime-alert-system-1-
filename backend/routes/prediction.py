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

@router.get("/districts")
def get_districts():
    from services.prediction import DATA
    return sorted(DATA["district"].unique().tolist())


@router.get("/crime-types")
def get_crime_types():
    from services.prediction import DATA
    return sorted(DATA["crime_type"].unique().tolist())