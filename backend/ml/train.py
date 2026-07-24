import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

from database import SessionLocal
import models


def get_risk_label(crime_count):
    if crime_count >= 15:
        return "High"
    elif crime_count >= 8:
        return "Medium"
    else:
        return "Low"


def train():
    db = SessionLocal()
    crimes = db.query(models.Crime).all()
    db.close()

    data = [{
        "district": c.district,
        "crime_type": c.crime_type,
        "crime_count": c.crime_count
    } for c in crimes]

    df = pd.DataFrame(data)
    df["risk"] = df["crime_count"].apply(get_risk_label)

    district_encoder = LabelEncoder()
    crime_type_encoder = LabelEncoder()

    df["district_enc"] = district_encoder.fit_transform(df["district"])
    df["crime_type_enc"] = crime_type_encoder.fit_transform(df["crime_type"])

    X = df[["district_enc", "crime_type_enc"]]
    y = df["risk"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, os.path.join(os.path.dirname(__file__), "model.pkl"))
    joblib.dump(district_encoder, os.path.join(os.path.dirname(__file__), "district_encoder.pkl"))
    joblib.dump(crime_type_encoder, os.path.join(os.path.dirname(__file__), "crime_type_encoder.pkl"))

    print(f"Model trained on {len(df)} records and saved to ml/model.pkl")


if __name__ == "__main__":
    train()