import pandas as pd
from database import SessionLocal, engine, Base
import models

Base.metadata.create_all(bind=engine)

CSV_PATH = "karnataka_crime_2024.csv"

def import_data():
    db = SessionLocal()
    db.query(models.Crime).delete()
    db.commit()

    df = pd.read_csv(CSV_PATH)

    records = []
    for _, row in df.iterrows():
        crime = models.Crime(
            district=row["district"],
            crime_type=row["crime_type"],
            crime_category=row["crime_category"],
            year=int(row["year"]),
            crime_count=int(row["crime_count"]),
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            crime_rate=float(row["crime_rate"]),
            ipc_cases=int(row["ipc_cases"]),
            sll_cases=int(row["sll_cases"]),
            total_cases=int(row["total_cases"]),
            conviction_rate=float(row["conviction_rate"]),
            chargesheet_rate=float(row["chargesheet_rate"]),
            pendency_rate=float(row["pendency_rate"]),
            police_range=row["police_range"],
            risk_level=row["risk_level"]
        )
        records.append(crime)

    db.add_all(records)
    db.commit()
    db.close()
    print(f"Imported {len(records)} crime records from {CSV_PATH}")

if __name__ == "__main__":
    import_data()