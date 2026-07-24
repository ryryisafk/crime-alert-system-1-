from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
import models
from routes import crimes, dashboard, hotspots, alerts, prediction

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Crime Early Warning API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crimes.router)
app.include_router(dashboard.router)
app.include_router(hotspots.router)
app.include_router(alerts.router)
app.include_router(prediction.router)

@app.get("/")
def home():
    return {
        "message": "Crime Early Warning Alert System API"
    }