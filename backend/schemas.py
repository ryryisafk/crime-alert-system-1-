import datetime
from pydantic import BaseModel


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

class DashboardSummary(BaseModel):
    total_crimes: int
    districts: int
    crime_types: int


class DistrictCount(BaseModel):
    district: str
    count: int


class MonthlyTrend(BaseModel):
    month: str
    count: int


class Hotspot(BaseModel):
    latitude: float
    longitude: float
    risk: str

class Alert(BaseModel):
    district: str
    crime_type: str
    risk: str
    reason: str

class PredictionRequest(BaseModel):
    district: str
    crime_type: str


class PredictionResponse(BaseModel):
    predicted_risk: str
    confidence: float