import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

from database import SessionLocal
import models


def train():
    db = SessionLocal()
    crimes = db.query(models.Crime).all()
    db.close()

    data = [{
        "district": c.district,
        "crime_type": c.crime_type,
        "crime_category": c.crime_category,
        "risk_level": c.risk_level
    } for c in crimes]

    df = pd.DataFrame(data)

    district_encoder = LabelEncoder()
    crime_type_encoder = LabelEncoder()
    category_encoder = LabelEncoder()

    df["district_enc"] = district_encoder.fit_transform(df["district"])
    df["crime_type_enc"] = crime_type_encoder.fit_transform(df["crime_type"])
    df["category_enc"] = category_encoder.fit_transform(df["crime_category"])

    X = df[["district_enc", "crime_type_enc", "category_enc"]]
    y = df["risk_level"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"Test accuracy: {accuracy:.2f}")

    ml_dir = os.path.dirname(__file__)
    joblib.dump(model, os.path.join(ml_dir, "model.pkl"))
    joblib.dump(district_encoder, os.path.join(ml_dir, "district_encoder.pkl"))
    joblib.dump(crime_type_encoder, os.path.join(ml_dir, "crime_type_encoder.pkl"))
    joblib.dump(category_encoder, os.path.join(ml_dir, "category_encoder.pkl"))

    print(f"Model trained on {len(df)} records and saved to ml/model.pkl")


if __name__ == "__main__":
    train()