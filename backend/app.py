from fastapi import FastAPI
from db import Base, engine
from routes import router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
