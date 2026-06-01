from sqlalchemy import Column, Integer, String, Float, Date

# BUG FIX: declarative_base moved in SQLAlchemy 1.4+; use the new import path
# to avoid deprecation warnings and breakage in SQLAlchemy 2.x.
from sqlalchemy.orm import declarative_base

from backend.db import Base

# =========================
# USERS
# =========================

class Users(Base):

    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))
    email    = Column(String(100), unique=True)
    password = Column(String(255))


# =========================
# DOCTORS
# =========================

class Doctors(Base):

    __tablename__ = "Doctors"

    doctor_id      = Column(Integer, primary_key=True, index=True)
    name           = Column(String(100))
    specialization = Column(String(100))
    hospital_name  = Column(String(150))
    city           = Column(String(100))
    rating         = Column(Float)
    latitude       = Column(Float)
    longitude      = Column(Float)


# =========================
# DOCTOR SCHEDULE
# =========================

class DoctorSchedule(Base):

    __tablename__ = "doctor_schedule"

    id          = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String(100))
    day_of_week = Column(String(20))
    slot        = Column(String(20))


# =========================
# APPOINTMENTS
# =========================

class Appointments(Base):

    __tablename__ = "appointments"

    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer)
    doctor_name = Column(String(100))
    hospital    = Column(String(150))
    date        = Column(Date)
    time        = Column(String(20))
    status      = Column(String(20))
