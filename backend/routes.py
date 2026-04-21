import sys
sys.path.append('../vector_search') 

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from db import SessionLocal
from models import Doctors
from vector_search import classify_message, get_chat_reply, explain_and_recommend, get_doctor
import re
from difflib import get_close_matches

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 Get all cities dynamically (normalized)
def get_all_cities(db):
    cities = db.query(Doctors.city).distinct().all()
    return list(set([c[0].strip().lower() for c in cities if c[0]]))


# 🔥 Extract city (case + typo + flexible)
def extract_city(text, db):
    text = text.lower()
    cities = get_all_cities(db)

    # pattern: from/in/at
    match = re.search(r"(?:from|in|at)\s+([a-z]+)", text)
    if match:
        word = match.group(1)
        best = get_close_matches(word, cities, n=1, cutoff=0.6)
        if best:
            return best[0]

    # fallback: scan all words
    words = re.findall(r"[a-z]+", text)
    for w in words:
        best = get_close_matches(w, cities, n=1, cutoff=0.75)
        if best:
            return best[0]

    return None


# 🔥 Extract hospital (case insensitive)
def extract_hospital(text, db):
    text = text.lower()
    hospitals = db.query(Doctors.hospital_name).distinct().all()
    hospitals = [h[0].strip().lower() for h in hospitals if h[0]]

    for h in hospitals:
        if h in text:
            return h
    return None


@router.post("/predict")
async def predict(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    message = data.get("symptom", "")

    try:
        
        vague_phrases = [
            "not well", "not feeling well", "feel sick", "feeling sick",
            "unwell", "not good", "feel bad", "feeling bad", "i'm sick",
            "i am sick", "something is wrong", "don't feel good",
            "not okay", "not ok", "feeling unwell", "im not well",
            "i am not well", "i'm not well"
        ]

        if any(phrase in message.lower() for phrase in vague_phrases):
            return {
                "type": "chat",
                "reply": "I'm sorry to hear that! Could you describe your symptoms in more detail? For example, do you have a headache, chest pain, fever, skin problem, or something else? 🩺"
            }
        
        # Step 2 — LLM classification
        classification = classify_message(message)

        if classification == "CHAT":
            return {
                "type": "chat",
                "reply": get_chat_reply(message)
            }

        elif classification == "QUESTION":
            return {
                "type": "chat",
                "reply": explain_and_recommend(message)
            }

        elif classification == "VAGUE":
            return {
                "type": "chat",
                "reply": "I'm sorry to hear that! Could you describe your symptoms in more detail? For example, do you have a headache, chest pain, fever, skin problem, or something else? 🩺"
            }
        
#3 SYMPTOM FLOW
        doctor_type = get_doctor(message)
        city = extract_city(message, db)
        hospital = extract_hospital(message, db)

        print("Detected city:", city)
        print("Detected hospital:", hospital)

        # 🔥 Base query
        query = db.query(Doctors).filter(
            func.lower(Doctors.specialization) == doctor_type.lower()
        )

        # 🔥 Priority 1: Hospital
        if hospital:
            query = query.filter(
                func.lower(Doctors.hospital_name).contains(hospital)
            )

        # 🔥 Priority 2: City
        elif city:
            query = query.filter(
                func.lower(Doctors.city) == city
            )

        doctors = query.order_by(Doctors.rating.desc()).all()

        # 🔥 Fallback: only specialization
        if not doctors:
            doctors = db.query(Doctors).filter(
                func.lower(Doctors.specialization) == doctor_type.lower()
            ).order_by(Doctors.rating.desc()).all()

        result = []

        for i, d in enumerate(doctors):
            result.append({
                "doctor": d.name or "Unknown",
                "hospital": d.hospital_name or "Unknown",
                "area": d.city or "Unknown",
                "rating": float(d.rating or 0),
                "speciality": d.specialization or "Unknown",
                "lat": float(d.latitude or 0),
                "lng": float(d.longitude or 0),
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
