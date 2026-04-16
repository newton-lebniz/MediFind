import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('Bhargav@2008')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
