import random
from datetime import date, timedelta

from database import SessionLocal, engine, Base
import models

Base.metadata.create_all(bind=engine)

districts = [
    "Trivandrum", "Kollam", "Pathanamthitta", "Alappuzha",
    "Kottayam", "Idukki", "Ernakulam", "Thrissur",
    "Palakkad", "Malappuram", "Kozhikode", "Wayanad",
    "Kannur", "Kasaragod"
]

crime_types = ["Theft", "Burglary", "Assault", "Fraud", "Vandalism", "Robbery"]

def seed():
    db = SessionLocal()

    db.query(models.Crime).delete()
    db.commit()

    start_date = date(2025, 1, 1)

    records = []
    for _ in range(300):
        random_days = random.randint(0, 570)
        record_date = start_date + timedelta(days=random_days)

        crime = models.Crime(
            district=random.choice(districts),
            crime_type=random.choice(crime_types),
            date=record_date,
            latitude=round(random.uniform(8.2, 12.8), 4),
            longitude=round(random.uniform(74.8, 77.4), 4),
            crime_count=random.randint(1, 20)
        )
        records.append(crime)

    db.add_all(records)
    db.commit()
    db.close()
    print(f"Seeded {len(records)} crime records.")

if __name__ == "__main__":
    seed()