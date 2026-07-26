import datetime
from pydantic import BaseModel


# ----------------------------
# Crime Schemas
# ----------------------------

class CrimeBase(BaseModel):
    district: str
    crime_type: str
    date: datetime.date | None = None
    latitude: float | None = None
    longitude: float | None = None
    crime_count: int | None = None


class CrimeCreate(CrimeBase):
    pass


class CrimeUpdate(BaseModel):
    district: str | None = None
    crime_type: str | None = None
    date: datetime.date | None = None
    latitude: float | None = None
    longitude: float | None = None
    crime_count: int | None = None


class CrimeResponse(CrimeBase):
    id: int

    class Config:
        from_attributes = True


# ----------------------------
# Dashboard Schemas
# ----------------------------

class DashboardSummary(BaseModel):
    total_crimes: int
    districts: int
    crime_types: int


class DistrictCount(BaseModel):
    district: str
    count: int

class CategoryCount(BaseModel):
    crime_type: str
    count: int


class MonthlyTrend(BaseModel):
    month: str
    count: int


class Hotspot(BaseModel):
    district: str

    latitude: float
    longitude: float

    risk: str

    crime_type: str
    crime_category: str

    crime_count: int
    crime_rate: float

    police_range: str

    conviction_rate: float
    chargesheet_rate: float
    pendency_rate: float


class Alert(BaseModel):
    district: str
    crime_type: str
    risk: str
    reason: str


# ----------------------------
# Prediction Schemas
# ----------------------------

class PredictionRequest(BaseModel):
    district: str
    crime_type: str


class AlertResponse(BaseModel):
    level: str
    message: str
    action: str


class PredictionResponse(BaseModel):
    predicted_risk: str
    confidence: float
    risk_score: int
    is_anomaly: bool

    district: str
    crime_type: str
    crime_category: str
    crime_count: int
    crime_rate: float
    police_range: str

    alert: AlertResponse