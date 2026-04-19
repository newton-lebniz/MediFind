from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from db import Base, engine
from routes import router

# ✅ create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ include routes
app.include_router(router)


# ✅ frontend
@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/chatpage")
def chat():
    return FileResponse("chat.html")
