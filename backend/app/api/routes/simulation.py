from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import Astronaut, Telemetry
from app.schemas.api import SimulationIn, TelemetryIn
from app.services.ml_service import analyze_simulation
router = APIRouter()

@router.post("/simulation/run")
def run_simulation(payload: SimulationIn, db: Session = Depends(get_db)):
    if not db.get(Astronaut, payload.astronaut_id):
        raise HTTPException(404, "Astronaut not found")
    history = db.query(Telemetry).filter_by(astronaut_id=payload.astronaut_id).order_by(Telemetry.timestamp.asc()).all()
    if not history:
        raise HTTPException(422, "No baseline telemetry available")
    allowed = {"heart_rate_bpm", "spo2_percent", "sleep_hours_last_24h", "body_temperature_celsius", "radiation_dose_rate_usv_per_hour", "activity_level_percent", "fatigue_level_0_10"}
    if not payload.metrics or set(payload.metrics) - allowed:
        raise HTTPException(422, "Provide supported hypothetical metric names only")
    original = {key: getattr(history[-1], key) for key in allowed}
    try:
        # Reuse telemetry Pydantic validation for hypothetical values.
        TelemetryIn(astronaut_id=payload.astronaut_id, **payload.metrics)
        baseline = analyze_simulation(payload.astronaut_id, {}, history)
        simulated = analyze_simulation(payload.astronaut_id, payload.metrics, history)
    except (ImportError, ModuleNotFoundError) as exc:
        raise HTTPException(503, f"ML module unavailable: {exc}")
    except ValueError as exc:
        raise HTTPException(422, str(exc))
    return {"astronaut_id": payload.astronaut_id, "baseline": baseline, "simulation": simulated,
            "changed_factors": {key: {"baseline": original.get(key), "simulated": value} for key, value in payload.metrics.items()}}
