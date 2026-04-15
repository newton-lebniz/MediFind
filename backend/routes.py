from fastapi import APIRouter, Depends
import sys
sys.path.append('../vector_search')
from vector_search import is_symptom, get_chat_reply, get_doctor

from sqlalchemy.orm import Session
import requests

from db import SessionLocal
from crud import insert_hospital
from models import Hospitals
from chatbot import ask_chatbot
from ml_model import train_model, predict_score

router = APIRouter()

GOOGLE_API_KEY = "AIzaSyB-CXbRUKUl4YRe3BqwB0YQ_2QgB838r_c"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 📍 GOOGLE API → STORE IN DB
@router.get("/fetch-google")
def fetch_google(lat: float, lng: float, db: Session = Depends(get_db)):

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=hospital&key={GOOGLE_API_KEY}"
    res = requests.get(url).json()

    count = 0

    for place in res.get("results", []):
        data = {
            "name": place.get("name"),
            "rating": place.get("rating", 0),
            "latitude": place["geometry"]["location"]["lat"],
            "longitude": place["geometry"]["location"]["lng"]
        }

        insert_hospital(db, data)
        count += 1

    return {"inserted": count}


# 🤖 ML RECOMMENDATION (FROM DB)
@router.get("/recommend")
def recommend(lat: float, lng: float, db: Session = Depends(get_db)):

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
            "name": h.name,
            "rating": h.rating,
            "score": round(score, 2)
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:10]
from fastapi import Request
from fastapi.responses import JSONResponse

@router.post("/predict")
async def predict(request: Request):
    data = await request.json()
    message = data.get("symptom", "")

    if not message:
        return JSONResponse({"error": "No message provided"}, status_code=400)

    try:
        if is_symptom(message):
            doctor_type = get_doctor(message)
            return {"type": "symptom", "doctor_type": doctor_type, "doctors": []}
        else:
            reply = get_chat_reply(message)
            return {"type": "chat", "reply": reply}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# 🧠 OPENAI CHATBOT
@router.get("/chat")
def chat(query: str):
    return {"response": ask_chatbot(query)}
