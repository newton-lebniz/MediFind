from sqlalchemy import Column, Integer, String, Float
from db import Base

# ✅ Doctors table
class Doctors(Base):
    __tablename__ = "Doctors"

    doctor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialization = Column(String)
    hospital_name = Column(String)
    city = Column(String)
    rating = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
