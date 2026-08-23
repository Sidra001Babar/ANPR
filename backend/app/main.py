from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.image import router as image_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(
    image_router
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "ANPR System API is running."
    }