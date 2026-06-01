from sqlalchemy.orm import Session
from models import Doctors


def insert_doctor(db: Session, data):

    existing = db.query(Doctors).filter(
        Doctors.name == data["name"],
        Doctors.hospital_name == data["hospital_name"]
    ).first()

    if existing:
        return

    doctor = Doctors(**data)

    db.add(doctor)
    db.commit()
