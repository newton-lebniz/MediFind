from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db import SessionLocal

from backend.models import (
    Users,
    Doctors,
    Appointments,
    DoctorSchedule
)

from backend.vector_search import (
    classify_message,
    generate_followup,
    get_doctor,
    get_chat_reply,
    explain_and_recommend
)

from pydantic import BaseModel
from typing import List, Optional

from datetime import date

import math

router = APIRouter()

# =========================================
# SCHEMAS
# =========================================

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class SymptomRequest(BaseModel):
    symptom: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    followup_stage: int = 0
    conversation: List[str] = []
    doctor_type: Optional[str] = None


class BookingRequest(BaseModel):
    user_id: int
    doctor_name: str
    hospital: str
    date: str
    time: str


# =========================================
# DATABASE
# =========================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================
# DISTANCE (Haversine)
# =========================================

def calculate_distance(lat1, lon1, lat2, lon2):

    if None in (lat1, lon1, lat2, lon2):
        return 9999

    R    = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# =========================================
# SIGNUP
# =========================================

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):

    existing = (
        db.query(Users)
        .filter(Users.email == data.email)
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = Users(
        username=data.username,
        email=data.email,
        password=data.password          # stored as-is — no hashing
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message":  "Signup successful",
        "id":       user.id,
        "username": user.username,
        "email":    user.email
    }


# =========================================
# LOGIN
# =========================================

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = (
        db.query(Users)
        .filter(Users.email == data.email)
        .first()
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Plain comparison — works for every account regardless of
    # when it was created, because we no longer hash anything.
    if user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "id":       user.id,
        "username": user.username,
        "email":    user.email
    }


# =========================================
# PREDICT
# =========================================

@router.post("/predict")
def predict(data: SymptomRequest):

    try:

        symptom      = data.symptom.strip()
        conversation = data.conversation.copy()
        stage        = data.followup_stage

        # ── First message ─────────────────────────────
        if stage == 0:

            classification = classify_message(symptom)
            print("CLASSIFICATION:", classification)

            if classification == "CHAT":
                return {
                    "success": True,
                    "type":    "chat",
                    "reply":   get_chat_reply(symptom)
                }

            if classification == "QUESTION":
                return {
                    "success": True,
                    "type":    "chat",
                    "reply":   explain_and_recommend(symptom)
                }

            if classification == "VAGUE":
                return {
                    "success": True,
                    "type":    "chat",
                    "reply":   "Could you describe your symptoms more clearly?"
                }

            if classification == "EMERGENCY":
                return {
                    "success": True,
                    "type":    "emergency",
                    "reply":   (
                        "🚨 This sounds like a medical emergency! "
                        "Please call emergency services immediately.\n\n"
                        "🇮🇳 India Emergency Numbers:\n"
                        "📞 Ambulance: 108\n"
                        "📞 National Emergency: 112\n"
                        "📞 Police: 100\n\n"
                        "Do not wait — call now or ask someone near you to help."
                    )
                }

            if classification == "SYMPTOM":
                conversation.append(symptom)
                question = generate_followup(" ".join(conversation))
                print("FOLLOWUP:", question)
                return {
                    "success":      True,
                    "type":         "followup_question",
                    "reply":        question,
                    "stage":        1,
                    "conversation": conversation
                }

            # fallback
            return {
                "success": True,
                "type":    "chat",
                "reply":   "Please explain your symptoms clearly."
            }

        # ── Followup continuation ──────────────────────
        conversation.append(symptom)

        if stage < 3:
            question = generate_followup(" ".join(conversation))
            print("FOLLOWUP:", question)
            return {
                "success":      True,
                "type":         "followup_question",
                "reply":        question,
                "stage":        stage + 1,
                "conversation": conversation
            }

        # ── Final recommendation ───────────────────────
        doctor_type = get_doctor(" ".join(conversation))

        return {
            "success":      True,
            "type":         "followup_complete",
            "reply":        f"Based on your symptoms, you may consult a {doctor_type}. Would you like doctor recommendations?",
            "doctor_type":  doctor_type,
            "conversation": conversation
        }

    except Exception as e:
        print("PREDICT ERROR:", str(e))
        return {
            "success": False,
            "type":    "chat",
            "reply":   "Server error"
        }


# =========================================
# RECOMMEND DOCTORS
# =========================================

@router.post("/recommend")
def recommend(data: SymptomRequest, db: Session = Depends(get_db)):

    doctor_type = data.doctor_type or get_doctor(data.symptom)

    doctors = (
        db.query(Doctors)
        .filter(Doctors.specialization.ilike(f"%{doctor_type}%"))
        .all()
    )

    results = []

    for d in doctors:

        distance = calculate_distance(
            data.lat, data.lng,
            d.latitude, d.longitude
        )

        results.append({
            "doctor":    d.name,
            "hospital":  d.hospital_name,
            "speciality": d.specialization,
            "area":      d.city,
            "rating":    d.rating,
            "distance":  distance,
            "maps":      f"https://www.google.com/maps/search/{d.latitude},{d.longitude}"
        })

    results.sort(key=lambda x: x["distance"])

    for i, r in enumerate(results):
        r["best"] = (i == 0)

    return {
        "type":        "symptom",
        "doctor_type": doctor_type,
        "doctors":     results[:5]
    }


# =========================================
# GET SLOTS
# =========================================

@router.get("/slots/{doctor_name}")
def get_slots(doctor_name: str, db: Session = Depends(get_db)):

    slots = (
        db.query(DoctorSchedule)
        .filter(DoctorSchedule.doctor_name == doctor_name)
        .all()
    )

    return {"slots": [s.slot for s in slots]}


# =========================================
# BOOK APPOINTMENT
# =========================================

@router.post("/book")
def book(data: BookingRequest, db: Session = Depends(get_db)):

    doctor = (
        db.query(Doctors)
        .filter(Doctors.name == data.doctor_name)
        .first()
    )

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    appointment = Appointments(
        user_id=data.user_id,
        doctor_name=data.doctor_name,
        hospital=data.hospital,
        date=data.date,
        time=data.time,
        status="Upcoming"
    )

    db.add(appointment)
    db.commit()

    return {"message": "Appointment booked"}


# =========================================
# GET APPOINTMENTS
# =========================================

@router.get("/appointments/{user_id}")
def get_appointments(user_id: int, db: Session = Depends(get_db)):

    appointments = (
        db.query(Appointments)
        .filter(Appointments.user_id == user_id)
        .all()
    )

    today    = str(date.today())
    upcoming = []
    previous = []

    for a in appointments:

        doctor = (
            db.query(Doctors)
            .filter(Doctors.name == a.doctor_name)
            .first()
        )

        city       = doctor.city            if doctor else ""
        speciality = doctor.specialization  if doctor else ""
        maps       = (
            f"https://www.google.com/maps/search/{doctor.latitude},{doctor.longitude}"
            if doctor else ""
        )

        obj = {
            "id":        a.id,
            "doctor":    a.doctor_name,
            "hospital":  a.hospital,
            "city":      city,
            "speciality": speciality,
            "date":      str(a.date),
            "time":      a.time,
            "maps":      maps
        }

        if str(a.date) >= today:
            upcoming.append(obj)
        else:
            previous.append(obj)

    return {"upcoming": upcoming, "previous": previous}


# =========================================
# CANCEL APPOINTMENT
# =========================================

@router.delete("/cancel/{appointment_id}")
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):

    appointment = (
        db.query(Appointments)
        .filter(Appointments.id == appointment_id)
        .first()
    )

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()

    return {"message": "Appointment cancelled"}
