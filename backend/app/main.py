
from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="COSMOCare API",
    description="Astronaut Health Monitoring and Risk Assessment System",
    version="1.0.0",
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to COSMOCare API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "COSMOCare Backend"
    }
