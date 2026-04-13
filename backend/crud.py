from sqlalchemy.orm import Session
from models import Hospitals

def insert_hospital(db: Session, data):
    existing = db.query(Hospitals).filter(Hospitals.name == data["name"]).first()

    if existing:
        return

    hospital = Hospitals(**data)
    db.add(hospital)
    db.commit()
