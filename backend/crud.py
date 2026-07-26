from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas

import os
import pandas as pd

DATASET = os.path.join(
    os.path.dirname(__file__),
    "ml",
    "../../CRIME_REVIEW_2021_TO_2024_KARNATAKA_CLEAN.csv"
)

MONTH_ORDER = {
    "JAN":1,
    "FEB":2,
    "MAR":3,
    "APR":4,
    "MAY":5,
    "JUN":6,
    "JUL":7,
    "AUG":8,
    "SEP":9,
    "OCT":10,
    "NOV":11,
    "DEC":12
}


def get_all_crimes(db: Session):
    return db.query(models.Crime).all()


def get_crime(db: Session, crime_id: int):
    return db.query(models.Crime).filter(models.Crime.id == crime_id).first()


def create_crime(db: Session, crime: schemas.CrimeCreate):
    db_crime = models.Crime(**crime.model_dump())
    db.add(db_crime)
    db.commit()
    db.refresh(db_crime)
    return db_crime


def update_crime(db: Session, crime_id: int, crime: schemas.CrimeUpdate):
    db_crime = get_crime(db, crime_id)
    if db_crime is None:
        return None
    for key, value in crime.model_dump(exclude_unset=True).items():
        setattr(db_crime, key, value)
    db.commit()
    db.refresh(db_crime)
    return db_crime


def delete_crime(db: Session, crime_id: int):
    db_crime = get_crime(db, crime_id)
    if db_crime is None:
        return None
    db.delete(db_crime)
    db.commit()
    return db_crime


def get_dashboard_summary(db: Session):
    total_crimes = db.query(func.sum(models.Crime.crime_count)).scalar() or 0
    districts = db.query(models.Crime.district).distinct().count()
    crime_types = db.query(models.Crime.crime_type).distinct().count()
    return {
        "total_crimes": total_crimes,
        "districts": districts,
        "crime_types": crime_types
    }


def get_crime_by_district(db: Session):
    results = (
        db.query(models.Crime.district, func.sum(models.Crime.crime_count).label("count"))
        .group_by(models.Crime.district)
        .order_by(func.sum(models.Crime.crime_count).desc())
        .all()
    )
    return [{"district": r.district, "count": r.count} for r in results]


def get_crime_by_category(db: Session):
    results = (
        db.query(models.Crime.crime_category, func.sum(models.Crime.crime_count).label("count"))
        .group_by(models.Crime.crime_category)
        .order_by(func.sum(models.Crime.crime_count).desc())
        .all()
    )
    return [{"crime_category": r.crime_category, "count": r.count} for r in results]


def get_hotspots(db: Session):

    crimes = db.query(models.Crime).all()

    return [

        {
            "district": crime.district,

            "latitude": crime.latitude,
            "longitude": crime.longitude,

            "risk": crime.risk_level,

            "crime_type": crime.crime_type,
            "crime_category": crime.crime_category,

            "crime_count": crime.crime_count,
            "crime_rate": crime.crime_rate,

            "police_range": crime.police_range,

            "conviction_rate": crime.conviction_rate,
            "chargesheet_rate": crime.chargesheet_rate,
            "pendency_rate": crime.pendency_rate,
        }

        for crime in crimes

    ]


def get_alerts(db: Session, pendency_threshold: float = 80.0, conviction_threshold: float = 40.0):
    all_crimes = db.query(models.Crime).all()
    alerts = []

    for c in all_crimes:
        if c.risk_level == "High" and c.pendency_rate and c.pendency_rate >= pendency_threshold:
            alerts.append({
                "district": c.district,
                "crime_type": c.crime_type,
                "risk": "High",
                "reason": f"{c.crime_type} in {c.district} is high risk with {c.pendency_rate}% case pendency"
            })
        elif c.risk_level == "High" and c.conviction_rate and c.conviction_rate <= conviction_threshold:
            alerts.append({
                "district": c.district,
                "crime_type": c.crime_type,
                "risk": "High",
                "reason": f"{c.crime_type} in {c.district} is high risk with only {c.conviction_rate}% conviction rate"
            })

    return alerts

def get_monthly_trend(db=None):
    df = pd.read_csv(DATASET)

    trend = (
        df.groupby(["Year", "Month"])["During the current month"]
          .sum()
          .reset_index()
    )

    trend["month_no"] = trend["Month"].map(MONTH_ORDER)

    trend = trend.sort_values(["Year", "month_no"])

    return [
        {
            "month": f"{row['Month']} {int(row['Year'])}",
            "count": int(row["During the current month"])
        }
        for _, row in trend.iterrows()
    ]