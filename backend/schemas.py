from pydantic import BaseModel


class CrimeBase(BaseModel):
    district: str
    crime_type: str
    crime_category: str | None = None
    year: int | None = None
    crime_count: int | None = None
    latitude: float | None = None
    longitude: float | None = None
    crime_rate: float | None = None
    ipc_cases: int | None = None
    sll_cases: int | None = None
    total_cases: int | None = None
    conviction_rate: float | None = None
    chargesheet_rate: float | None = None
    pendency_rate: float | None = None
    police_range: str | None = None
    risk_level: str | None = None


class CrimeCreate(CrimeBase):
    pass


class CrimeUpdate(BaseModel):
    district: str | None = None
    crime_type: str | None = None
    crime_category: str | None = None
    year: int | None = None
    crime_count: int | None = None
    latitude: float | None = None
    longitude: float | None = None
    crime_rate: float | None = None
    ipc_cases: int | None = None
    sll_cases: int | None = None
    total_cases: int | None = None
    conviction_rate: float | None = None
    chargesheet_rate: float | None = None
    pendency_rate: float | None = None
    police_range: str | None = None
    risk_level: str | None = None


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


class CategoryCount(BaseModel):
    crime_category: str
    count: int


class Hotspot(BaseModel):
    district: str
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