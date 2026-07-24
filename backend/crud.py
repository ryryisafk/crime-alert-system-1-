from sqlalchemy.orm import Session
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

from sqlalchemy import func


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


def get_monthly_trend(db: Session):
    results = (
        db.query(
            func.strftime("%Y-%m", models.Crime.date).label("month"),
            func.sum(models.Crime.crime_count).label("count")
        )
        .group_by("month")
        .order_by("month")
        .all()
    )
    return [{"month": r.month, "count": r.count} for r in results]

def get_hotspots(db: Session, threshold_high: int = 15, threshold_medium: int = 8):
    results = db.query(models.Crime).all()
    hotspots = []
    for r in results:
        if r.crime_count >= threshold_high:
            risk = "High"
        elif r.crime_count >= threshold_medium:
            risk = "Medium"
        else:
            risk = "Low"
        hotspots.append({
            "latitude": r.latitude,
            "longitude": r.longitude,
            "risk": risk
        })
    return hotspots

from datetime import date as date_cls, timedelta


def get_alerts(db: Session, recent_days: int = 30, spike_threshold: float = 30.0):
    today = date_cls.today()
    recent_start = today - timedelta(days=recent_days)
    previous_start = recent_start - timedelta(days=recent_days)

    all_crimes = db.query(models.Crime).all()

    recent_totals = {}
    previous_totals = {}

    for c in all_crimes:
        if c.date is None:
            continue
        key = (c.district, c.crime_type)
        if recent_start <= c.date <= today:
            recent_totals[key] = recent_totals.get(key, 0) + (c.crime_count or 0)
        elif previous_start <= c.date < recent_start:
            previous_totals[key] = previous_totals.get(key, 0) + (c.crime_count or 0)

    alerts = []
    for key, recent_count in recent_totals.items():
        district, crime_type = key
        previous_count = previous_totals.get(key, 0)

        if previous_count == 0:
            if recent_count > 0:
                alerts.append({
                    "district": district,
                    "crime_type": crime_type,
                    "risk": "High",
                    "reason": f"{crime_type} newly emerged with {recent_count} cases in the last {recent_days} days"
                })
            continue

        percent_change = ((recent_count - previous_count) / previous_count) * 100

        if percent_change >= spike_threshold:
            risk = "High" if percent_change >= spike_threshold * 2 else "Medium"
            alerts.append({
                "district": district,
                "crime_type": crime_type,
                "risk": risk,
                "reason": f"{crime_type} increased by {percent_change:.0f}% in {district}"
            })

    alerts.sort(key=lambda a: a["risk"] == "High", reverse=True)
    return alerts

