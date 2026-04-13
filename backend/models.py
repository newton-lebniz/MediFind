from sqlalchemy import Column, Integer, String, Float
from db import Base

class Hospitals(Base):
    __tablename__ = "Hospitals"

    hospital_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rating = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
