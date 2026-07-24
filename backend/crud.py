from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas


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


RISK_ORDER = {"Low": 0, "Medium": 1, "High": 2}


def get_hotspots(db: Session):
    all_crimes = db.query(models.Crime).all()
    district_risk = {}

    for c in all_crimes:
        current = district_risk.get(c.district)
        if current is None or RISK_ORDER.get(c.risk_level, 0) > RISK_ORDER.get(current["risk"], 0):
            district_risk[c.district] = {
                "district": c.district,
                "latitude": c.latitude,
                "longitude": c.longitude,
                "risk": c.risk_level
            }

    return list(district_risk.values())


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