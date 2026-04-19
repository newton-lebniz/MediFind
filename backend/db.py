import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Get values
user = os.getenv("MYSQL_USER")
raw_password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
db = os.getenv("MYSQL_DB")

print("RAW PASSWORD:", raw_password)  # debug

# Encode password (important for @)
password = quote_plus(raw_password)

# Create DB URL
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}/{db}"

print("DB URL:", DATABASE_URL)

# Create engine
engine = create_engine(DATABASE_URL)

# Session
SessionLocal = sessionmaker(bind=engine)

# Base (IMPORTANT)
Base = declarative_base()
