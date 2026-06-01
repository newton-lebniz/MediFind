from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.routes import router

app = FastAPI()

app.include_router(router)

# =========================
# STATIC
# =========================

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)

# =========================
# LOGIN PAGE
# =========================

@app.get("/")
async def home():

    return FileResponse(
        "frontend/index.html"
    )

# =========================
# CHAT PAGE
# =========================

@app.get("/chatpage")
async def chatpage():

    return FileResponse(
        "frontend/chat.html"
    )
