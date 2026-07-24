from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary", response_model=schemas.DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)):
    return crud.get_dashboard_summary(db)


@router.get("/crime-by-district", response_model=list[schemas.DistrictCount])
def crime_by_district(db: Session = Depends(get_db)):
    return crud.get_crime_by_district(db)


@router.get("/monthly-trend", response_model=list[schemas.MonthlyTrend])
def monthly_trend(db: Session = Depends(get_db)):
    return crud.get_monthly_trend(db)