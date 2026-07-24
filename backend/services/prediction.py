import os
import joblib

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "ml")

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
district_encoder = joblib.load(os.path.join(BASE_DIR, "district_encoder.pkl"))
crime_type_encoder = joblib.load(os.path.join(BASE_DIR, "crime_type_encoder.pkl"))


def predict_risk(district: str, crime_type: str):
    try:
        district_enc = district_encoder.transform([district])[0]
    except ValueError:
        return None, None

    try:
        crime_type_enc = crime_type_encoder.transform([crime_type])[0]
    except ValueError:
        return None, None

    X = [[district_enc, crime_type_enc]]
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    confidence = round(max(probabilities), 2)

    return prediction, confidence