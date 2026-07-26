import os
import joblib
import pandas as pd

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "ml")

DATA = pd.read_csv(os.path.join(BASE_DIR, "../../karnataka_crime_2024.csv"))

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
anomaly = joblib.load(os.path.join(BASE_DIR, "anomaly.pkl"))


def predict_risk(request):

    # Find matching district + crime type (case-insensitive)
    matches = DATA[
        (DATA["district"].str.lower() == request.district.lower()) &
        (DATA["crime_type"].str.lower() == request.crime_type.lower())
    ]

    # No matching data found
    if matches.empty:
        return {
            "predicted_risk": "Unknown",
            "confidence": 0.0,
            "risk_score": 0,
            "is_anomaly": False,
            "district": request.district,
            "crime_type": request.crime_type,
            "crime_count": None,
            "police_range": None,
            "alert": {
                "level": "LOW",
                "message": "No matching crime data found.",
                "action": "Please choose a valid district and crime type."
            }
        }

    # Use the first matching row
    row = matches.iloc[0]

    # Build model input exactly as it was trained
    sample = pd.DataFrame([{
        "district": row["district"],
        "crime_type": row["crime_type"],
        "crime_category": row["crime_category"],

        "crime_count": row["crime_count"],
        "crime_rate": row["crime_rate"],

        "ipc_cases": row["ipc_cases"],
        "sll_cases": row["sll_cases"],
        "total_cases": row["total_cases"],

        "conviction_rate": row["conviction_rate"],
        "chargesheet_rate": row["chargesheet_rate"],
        "pendency_rate": row["pendency_rate"],

        "police_range": row["police_range"]
    }])

    # Predict risk
    prediction = model.predict(sample)[0]

    # Confidence
    confidence = float(max(model.predict_proba(sample)[0]))

    # Anomaly detection
    processed = model.named_steps["preprocessor"].transform(sample)
    anomaly_result = anomaly.predict(processed)[0]
    is_anomaly = anomaly_result == -1

    # Risk score
    risk_score = round(confidence * 100)

    if prediction == "High":
        risk_score += 10
    elif prediction == "Medium":
        risk_score += 5

    risk_score = min(risk_score, 100)

    # Alert generation
    if is_anomaly:
        alert = {
            "level": "HIGH",
            "message": "Unusual crime pattern detected.",
            "action": "Notify police immediately."
        }

    elif prediction == "High":
        alert = {
            "level": "HIGH",
            "message": "High crime risk detected.",
            "action": "Increase police patrol."
        }

    elif prediction == "Medium":
        alert = {
            "level": "MEDIUM",
            "message": "Moderate crime risk.",
            "action": "Monitor area."
        }

    else:
        alert = {
            "level": "LOW",
            "message": "Area currently safe.",
            "action": "Routine monitoring."
        }

    return {
        "predicted_risk": prediction,
        "confidence": round(confidence, 2),
        "risk_score": risk_score,
        "is_anomaly": is_anomaly,

        # Extra information for frontend
        "district": row["district"],
        "crime_type": row["crime_type"],
        "crime_category": row["crime_category"],
        "crime_count": int(row["crime_count"]),
        "crime_rate": float(row["crime_rate"]),
        "police_range": row["police_range"],

        "alert": alert
    }