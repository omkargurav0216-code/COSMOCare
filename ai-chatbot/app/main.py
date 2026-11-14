
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router

app = FastAPI(
    title="COSMOCare AI Service",
    description=(
        "Independent AI service for COSMOCare's "
        "Astronaut Health Monitoring and Risk Assessment System."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization", "X-Internal-Token"],
)

app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "COSMOCare AI Service",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "COSMOCare AI",
    }
