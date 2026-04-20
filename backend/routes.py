import sys
sys.path.append('../vector_search')
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Doctors
from vector_search import is_symptom, get_chat_reply, get_doctor
import re
from difflib import get_close_matches

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 Supported cities (must match DB)
KNOWN_CITIES = ["raichur", "mumbai", "bangalore", "hyderabad", "delhi", "kolkata"]


# 🔥 Smart city extraction (case + typo tolerant)
def extract_city(text):
    text = text.lower()

    # pattern-based extraction
    match = re.search(r"(?:from|in|at)\s+([a-z]+)", text)
    if match:
        word = match.group(1)
        best = get_close_matches(word, KNOWN_CITIES, n=1, cutoff=0.6)
        return best[0] if best else None

    # fallback: scan words
    words = re.findall(r"[a-z]+", text)
    for w in words:
        best = get_close_matches(w, KNOWN_CITIES, n=1, cutoff=0.75)
        if best:
            return best[0]

    return None


@router.post("/predict")
async def predict(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    message = data.get("symptom", "")

    try:
        # 💬 CHAT MODE
        if not is_symptom(message):
            return {
                "type": "chat",
                "reply": get_chat_reply(message)
            }

        doctor_type = get_doctor(message)
        city = extract_city(message)

        print("Detected city:", city)

        # 🔥 STRICT FILTER (city + specialization)
        if city:
            doctors = db.query(Doctors).filter(
                Doctors.specialization == doctor_type,
                Doctors.city.ilike(f"%{city}%")
            ).order_by(Doctors.rating.desc()).all()
        else:
            doctors = db.query(Doctors).filter(
                Doctors.specialization == doctor_type
            ).order_by(Doctors.rating.desc()).all()

        # 🔥 FALLBACK if no doctors in city
        if not doctors:
            doctors = db.query(Doctors).filter(
                Doctors.specialization == doctor_type
            ).order_by(Doctors.rating.desc()).all()

        result = []

        for i, d in enumerate(doctors):
            result.append({
                "doctor": d.name,
                "hospital": d.hospital_name,
                "area": d.city,
                "rating": d.rating,
                "speciality": d.specialization,
                "best": True if i == 0 else False
            })

        return {
            "type": "symptom",
            "doctor_type": doctor_type,
            "doctors": result[:5]
        }

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}
