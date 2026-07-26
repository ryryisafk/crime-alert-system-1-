import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier, IsolationForest

DATASET = os.path.join(os.path.dirname(__file__), "../karnataka_crime_2024.csv")

df = pd.read_csv(DATASET)

features = [
    "district",
    "crime_type",
    "crime_category",
    "crime_count",
    "crime_rate",
    "ipc_cases",
    "sll_cases",
    "total_cases",
    "conviction_rate",
    "chargesheet_rate",
    "pendency_rate",
    "police_range"
]

target = "risk_level"

X = df[features]
y = df[target]

categorical = [
    "district",
    "crime_type",
    "crime_category",
    "police_range"
]

numerical = [
    "crime_count",
    "crime_rate",
    "ipc_cases",
    "sll_cases",
    "total_cases",
    "conviction_rate",
    "chargesheet_rate",
    "pendency_rate"
]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numerical)
    ]
)

classifier = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ))
])

classifier.fit(X, y)

joblib.dump(classifier, "model.pkl")

X_processed = preprocessor.fit_transform(X)

anomaly_model = IsolationForest(
    contamination=0.05,
    random_state=42
)

anomaly_model.fit(X_processed)

joblib.dump(anomaly_model, "anomaly.pkl")

print("Training Complete")