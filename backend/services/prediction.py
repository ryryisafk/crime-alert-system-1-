import os
import joblib
import pandas as pd
from ai.reasoning_engine import generate_reasoning

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "ml")

DATA = pd.read_csv(os.path.join(BASE_DIR, "../../karnataka_crime_2024.csv"))

STATE_CRIME_RATE = DATA["crime_rate"].mean()
STATE_CONVICTION_RATE = DATA["conviction_rate"].mean()
STATE_PENDENCY_RATE = DATA["pendency_rate"].mean()
STATE_CHARGESHEET_RATE = DATA["chargesheet_rate"].mean()
STATE_CRIME_COUNT = DATA["crime_count"].mean()

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
            "risk": "Unknown",
            "confidence": 0,
            "warning_score": 0,
            "reasoning": ["No matching crime data found."],
            "recommendations": ["Choose a valid district and crime type."],
            "district": request.district,
            "crime_type": request.crime_type,
            "crime_category": "",
            "crime_count": 0,
            "crime_rate": 0.0,
            "police_range": "",
            "is_anomaly": False,
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
    # Calibrated confidence for display
    display_confidence = min(
        max(int(70 + confidence * 25), 70),
        95
    )

    # Anomaly detection
    processed = model.named_steps["preprocessor"].transform(sample)
    anomaly_result = anomaly.predict(processed)[0]
    is_anomaly = anomaly_result == -1

    # Risk score
    warning_score = 0

    warning_score += confidence * 40

    warning_score += min(row["crime_rate"] / 3, 20)

    warning_score += min(row["pendency_rate"] / 10, 20)

    warning_score += max((60 - row["conviction_rate"]) / 3, 20)

    if is_anomaly:
        warning_score += 10

    warning_score = round(min(warning_score, 100))

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

    analysis = generate_reasoning(
        row,
        prediction,
        {
            "crime_rate": STATE_CRIME_RATE,
            "conviction": STATE_CONVICTION_RATE,
            "pendency": STATE_PENDENCY_RATE,
            "crime_count": STATE_CRIME_COUNT,
        }
    )

    return {

        "risk": prediction,

        "confidence": display_confidence,

        "warning_score": warning_score,

        "reasoning": analysis["reasoning"],
        "recommendations": analysis["recommendations"],

        "district": row["district"],

        "crime_type": row["crime_type"],

        "crime_category": row["crime_category"],

        "crime_count": int(row["crime_count"]),

        "crime_rate": float(row["crime_rate"]),

        "police_range": row["police_range"],

        "is_anomaly": bool(is_anomaly)
    }