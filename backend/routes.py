from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import requests
import os
from dotenv import load_dotenv

from db import SessionLocal
from crud import insert_hospital
from models import Hospitals
from ml_model import train_model, predict_score

import sys
sys.path.append('../vector_search')
from vector_search import is_symptom, get_chat_reply, get_doctor

router = APIRouter()
load_dotenv()

GOOGLE_API_KEY = os.getenv("AIzaSyB-CXbRUKUl4YRe3BqwB0YQ_2QgB838r_c")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 📍 GOOGLE FETCH + AUTO INSERT
def fetch_and_store(lat, lng, db):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=hospital&key={GOOGLE_API_KEY}"
    
    res = requests.get(url).json()

    for place in res.get("results", []):
        data = {
            "hospital_name": place.get("name"),
            "city": "Unknown",
            "rating": place.get("rating", 0),
            "latitude": place["geometry"]["location"]["lat"],
            "longitude": place["geometry"]["location"]["lng"]
        }

        insert_hospital(db, data)


# 🤖 MAIN API (GPS + ML + INSERT)
@router.post("/predict")
async def predict(request: Request, db: Session = Depends(get_db)):

    body = await request.json()

    message = body.get("symptom", "")
    lat = body.get("lat")
    lng = body.get("lng")

    # fallback if GPS not available
    if not lat or not lng:
        lat, lng = 12.9716, 77.5946

    # 🔥 AUTO INSERT USING GPS
    fetch_and_store(lat, lng, db)

    # SYMPTOM → DOCTOR
    if is_symptom(message):
        doctor_type = get_doctor(message)

        hospitals = db.query(Hospitals).all()

        dataset = []
        results = []

        for h in hospitals:
            distance = ((lat - h.latitude)**2 + (lng - h.longitude)**2)**0.5

            dataset.append({
                "rating": h.rating or 0,
                "distance": distance
            })

        train_model(dataset)

        for h in hospitals:
            distance = ((lat - h.latitude)**2 + (lng - h.longitude)**2)**0.5
            score = predict_score(h.rating or 0, distance)

            results.append({
                "name": h.hospital_name,
                "city": h.city,
                "rating": h.rating,
                "distance": round(distance, 2),
                "score": round(score, 2)
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        return {
            "type": "symptom",
            "doctor_type": doctor_type,
            "doctors": results[:5]
        }

    # NORMAL CHAT
    else:
        reply = get_chat_reply(message)
        return {"type": "chat", "reply": reply}
