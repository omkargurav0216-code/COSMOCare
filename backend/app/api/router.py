
from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/status")
def get_api_status():
    return {
        "status": "API router connected",
        "service": "COSMOCare"
    }
