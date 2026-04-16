from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from db import Base, engine
from routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Serve frontend
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("../frontend/index.html")

@app.get("/chat")
def chat_page():
    return FileResponse("../frontend/chat.html")