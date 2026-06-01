import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# FIX: declarative_base moved to sqlalchemy.orm in SQLAlchemy 1.4+
# The old sqlalchemy.ext.declarative path is removed in SQLAlchemy 2.x.
from sqlalchemy.orm import declarative_base

from urllib.parse import quote_plus

load_dotenv()

MYSQL_USER     = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST     = os.getenv("MYSQL_HOST")
MYSQL_DB       = os.getenv("MYSQL_DB")

# Encode special characters in password (e.g. @, #, %)
ENCODED_PASSWORD = quote_plus(MYSQL_PASSWORD)

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{MYSQL_USER}:"
    f"{ENCODED_PASSWORD}@"
    f"{MYSQL_HOST}/"
    f"{MYSQL_DB}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
