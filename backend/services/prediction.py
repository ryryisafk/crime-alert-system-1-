import os
import joblib

from database import SessionLocal
import models

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "ml")

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
district_encoder = joblib.load(os.path.join(BASE_DIR, "district_encoder.pkl"))
crime_type_encoder = joblib.load(os.path.join(BASE_DIR, "crime_type_encoder.pkl"))
category_encoder = joblib.load(os.path.join(BASE_DIR, "category_encoder.pkl"))


def _get_category_lookup():
    db = SessionLocal()
    rows = db.query(models.Crime.district, models.Crime.crime_type, models.Crime.crime_category).all()
    db.close()
    return {(r.district, r.crime_type): r.crime_category for r in rows}


category_lookup = _get_category_lookup()


def predict_risk(district: str, crime_type: str):
    crime_category = category_lookup.get((district, crime_type))
    if crime_category is None:
        return None, None

    try:
        district_enc = district_encoder.transform([district])[0]
        crime_type_enc = crime_type_encoder.transform([crime_type])[0]
        category_enc = category_encoder.transform([crime_category])[0]
    except ValueError:
        return None, None

    X = [[district_enc, crime_type_enc, category_enc]]
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    confidence = round(max(probabilities), 2)

    return prediction, confidence