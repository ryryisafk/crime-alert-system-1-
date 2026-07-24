from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("/", response_model=list[schemas.Alert])
def get_alerts(db: Session = Depends(get_db)):
    return crud.get_alerts(db)