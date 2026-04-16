from sqlalchemy import Column, Integer, String, Float
from db import Base

class Hospitals(Base):
    __tablename__ = "Hospitals"

    hospital_id = Column(Integer, primary_key=True, index=True)
    hospital_name = Column(String(100))
    city = Column(String(50))
    rating = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
