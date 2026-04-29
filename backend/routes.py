import sys
sys.path.append('../vector_search') 

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from db import SessionLocal
from models import Doctors
from vector_search import classify_message, get_chat_reply, get_chat_reply_with_history, explain_and_recommend, get_doctor, triage_symptom , extract_symptoms
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
    if not message.strip():
     return {"type": "chat", "reply": "Please describe your symptoms so I can help you."}
    history = data.get("history", [])
    waiting_for_city = data.get("waiting_for_city", False)
    doctor_type_pending = data.get("doctor_type", None)
    offer_accepted = data.get("offer_accepted", False)

    # EMERGENCY — always first
    emergency_keywords = [
        "took too many pills", "too many pills", "overdosed", "overdose",
    "can't breathe", "cannot breathe", "shortness of breath", "airway blocked",
    "choking", "someone is choking", "choking me", "suffocating", "drowning",
    "coughing blood", "vomiting blood", "spitting blood", "heavy bleeding",
    "bleeding heavily", "won't stop bleeding",
    "heart attack", "severe chest pain", "chest pain right now",
    "tight chest", "chest pressure", "left arm pain",
    "unconscious", "fainted", "passed out", "blacked out",
    "stabbed", "shot", "being attacked", "can't swallow", "throat blocked",
    "stuck in", "stuck up", "foreign body", "bottle stuck", "something stuck",
    "stroke", "face drooping", "arm weak", "speech slurred",
    "poisoned", "swallowed poison",
    "paralyzed", "can't move", "seizure", "fits", "convulsions"
    ]
    
    if any(kw in message.lower() for kw in emergency_keywords):
        return {
            "type": "chat",
            "reply": "🚨 This sounds like a medical emergency! Please call 112 immediately or go to your nearest emergency room. Do not wait. 🚨"
        }

    # CRISIS
    crisis_keywords = ["kill myself", "suicide", "end my life", "want to die", "hurt myself", "self harm"]
    if any(kw in message.lower() for kw in crisis_keywords):
        return {
            "type": "chat",
            "reply": "I'm really concerned. Please call iCall at 9152987821 immediately — free and confidential. You are not alone. 💙"
        }

    try:
        # User accepted doctor offer — ask for city
        if offer_accepted and doctor_type_pending:
            return {
                "type": "ask_city",
                "doctor_type": doctor_type_pending,
                "reply": f"Great! Which city are you in? I'll find the best {doctor_type_pending} near you."
            }

        # User gave city — show doctors
        if waiting_for_city and doctor_type_pending:
             # Reject nonsense city inputs
            invalid_inputs = ["ok", "okay", "yes", "no", "sure", "fine", "k", "hmm", "idk"]
            if message.strip().lower() in invalid_inputs:
                  return {
            "type": "ask_city",
            "doctor_type": doctor_type_pending,
            "reply": "I didn't catch that — could you tell me which city you're in? For example: Raichur, Bangalore, Mumbai."
        }

            city = extract_city(message, db)
            if not city:
                city = message.strip().capitalize()
            doctors = db.query(Doctors).filter(
                func.lower(Doctors.specialization) == doctor_type_pending.lower(),
                func.lower(Doctors.city) == city.lower()
            ).order_by(Doctors.rating.desc()).all()
            if not doctors:
                doctors = db.query(Doctors).filter(
                    func.lower(Doctors.specialization) == doctor_type_pending.lower()
                ).order_by(Doctors.rating.desc()).all()
            result = [{"doctor": d.name, "hospital": d.hospital_name,
                       "area": d.city, "rating": float(d.rating),
                       "speciality": d.specialization, "best": i == 0}
                      for i, d in enumerate(doctors)]
            return {"type": "symptom", "doctor_type": doctor_type_pending, "doctors": result[:5]}

        classification = classify_message(message)

        if classification == "EMERGENCY":
            return {
                "type": "chat",
                "reply": "🚨 This sounds serious! Please call 112 immediately or go to your nearest emergency room. Do not wait. 🚨"
            }

        elif classification == "CHAT":
            return {"type": "chat", "reply": get_chat_reply_with_history(message, history)}

        elif classification == "QUESTION":
            return {"type": "chat", "reply": explain_and_recommend(message)}

        elif classification == "VAGUE":
            return {"type": "chat", "reply": get_chat_reply_with_history(message, history)}

        # SYMPTOM FLOW — triage first, offer doctors
        doctor_type = get_doctor(extract_symptoms(message))
        triage_reply = triage_symptom(message, history)

        return {
            "type": "offer_doctors",
            "doctor_type": doctor_type,
            "reply": triage_reply
        }

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}