from fastapi import APIRouter
from app.api.routes import astronauts, telemetry, risks, alerts, simulation, chat
api_router=APIRouter()
api_router.include_router(astronauts.router,tags=["astronauts"])
api_router.include_router(telemetry.router,tags=["telemetry"])
api_router.include_router(risks.router,tags=["risk"])
api_router.include_router(alerts.router,tags=["alerts"])
api_router.include_router(simulation.router,tags=["simulation"])
api_router.include_router(chat.router,tags=["chat"])
