from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Crime(Base):
    __tablename__ = "crimes"

    id = Column(Integer, primary_key=True, index=True)

    district = Column(String, nullable=False)

    crime_type = Column(String, nullable=False)

    date = Column(Date)

    latitude = Column(Float)

    longitude = Column(Float)

    crime_count = Column(Integer)