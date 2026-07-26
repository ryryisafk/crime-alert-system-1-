import os
import joblib
import pandas as pd

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "ml")

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
anomaly = joblib.load(os.path.join(BASE_DIR, "anomaly.pkl"))


def predict_risk(request):

    sample = pd.DataFrame([{
        "district": request.district,
        "crime_type": request.crime_type,
        "crime_category": request.crime_category,
        "crime_count": request.crime_count,
        "crime_rate": request.crime_rate,
        "ipc_cases": request.ipc_cases,
        "sll_cases": request.sll_cases,
        "total_cases": request.total_cases,
        "conviction_rate": request.conviction_rate,
        "chargesheet_rate": request.chargesheet_rate,
        "pendency_rate": request.pendency_rate,
        "police_range": request.police_range
    }])

    prediction = model.predict(sample)[0]

    confidence = float(max(model.predict_proba(sample)[0]))

    processed = model.named_steps["preprocessor"].transform(sample)

    anomaly_result = anomaly.predict(processed)[0]

    is_anomaly = anomaly_result == -1

    risk_score = round(confidence * 100)

    if prediction == "High":
        risk_score += 10
    elif prediction == "Medium":
        risk_score += 5

    risk_score = min(risk_score, 100)

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
        "alert": alert
    }