from sqlalchemy.orm import Session
from models import Hospitals

def insert_hospital(db: Session, data):
    existing = db.query(Hospitals).filter(
        Hospitals.hospital_name == data["hospital_name"],
        Hospitals.latitude == data["latitude"],
        Hospitals.longitude == data["longitude"]
    ).first()

    if existing:
        return

    db.add(Hospitals(**data))
    db.commit()
