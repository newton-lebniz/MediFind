from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Doctors
from vector_search import is_symptom, get_chat_reply, get_doctor
import re

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ FIXED city extraction
def extract_city(text):
    text = text.lower()
    match = re.search(r"(?:from|in|at)\s+([a-z]+)", text)
    return match.group(1) if match else None


@router.post("/predict")
async def predict(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    message = data.get("symptom", "")

    try:
        # chat
        if not is_symptom(message):
            return {
                "type": "chat",
                "reply": get_chat_reply(message)
            }

        doctor_type = get_doctor(message)
        city = extract_city(message)

        print("Detected city:", city)

        # 🔥 STRICT FILTER FIRST
        if city:
            doctors = db.query(Doctors).filter(
                Doctors.specialization == doctor_type,
                Doctors.city.ilike(f"%{city}%")
            ).order_by(Doctors.rating.desc()).all()
        else:
            doctors = db.query(Doctors).filter(
                Doctors.specialization == doctor_type
            ).order_by(Doctors.rating.desc()).all()

        # 🔥 FALLBACK
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
