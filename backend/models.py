from sqlalchemy import Column, Integer, String, Float
from database import Base

class Crime(Base):
    __tablename__ = "crimes"

    id = Column(Integer, primary_key=True, index=True)
    district = Column(String, nullable=False)
    crime_type = Column(String, nullable=False)
    crime_category = Column(String)
    year = Column(Integer)
    crime_count = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    crime_rate = Column(Float)
    ipc_cases = Column(Integer)
    sll_cases = Column(Integer)
    total_cases = Column(Integer)
    conviction_rate = Column(Float)
    chargesheet_rate = Column(Float)
    pendency_rate = Column(Float)
    police_range = Column(String)
    risk_level = Column(String)