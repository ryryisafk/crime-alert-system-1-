from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
)


@router.get("/", response_model=list[schemas.Hotspot])
def hotspots(db: Session = Depends(get_db)):
    return crud.get_hotspots(db)