from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/crimes",
    tags=["Crimes"]
)


@router.get("/", response_model=list[schemas.CrimeResponse])
def get_crimes(db: Session = Depends(get_db)):
    return crud.get_all_crimes(db)


@router.post("/", response_model=schemas.CrimeResponse)
def create_crime(crime: schemas.CrimeCreate, db: Session = Depends(get_db)):
    return crud.create_crime(db, crime)


@router.get("/{crime_id}", response_model=schemas.CrimeResponse)
def get_crime(crime_id: int, db: Session = Depends(get_db)):
    db_crime = crud.get_crime(db, crime_id)
    if db_crime is None:
        raise HTTPException(status_code=404, detail="Crime not found")
    return db_crime


@router.put("/{crime_id}", response_model=schemas.CrimeResponse)
def update_crime(crime_id: int, crime: schemas.CrimeUpdate, db: Session = Depends(get_db)):
    db_crime = crud.update_crime(db, crime_id, crime)
    if db_crime is None:
        raise HTTPException(status_code=404, detail="Crime not found")
    return db_crime


@router.delete("/{crime_id}")
def delete_crime(crime_id: int, db: Session = Depends(get_db)):
    db_crime = crud.delete_crime(db, crime_id)
    if db_crime is None:
        raise HTTPException(status_code=404, detail="Crime not found")
    return {"message": "Crime deleted successfully"}