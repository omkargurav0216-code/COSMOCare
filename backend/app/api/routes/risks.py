from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import Astronaut,RiskAssessment
from app.services.risk_service import run_assessment
from app.schemas.api import RiskOut
router=APIRouter()
@router.get("/astronauts/{astronaut_id}/risk",response_model=list[RiskOut])
def risk_history(astronaut_id:str,db:Session=Depends(get_db)):
    if not db.get(Astronaut,astronaut_id): raise HTTPException(404,"Astronaut not found")
    return db.query(RiskAssessment).filter_by(astronaut_id=astronaut_id).order_by(RiskAssessment.created_at.desc()).limit(100).all()
@router.post("/astronauts/{astronaut_id}/risk/analyze",response_model=RiskOut)
def analyze_risk(astronaut_id:str,db:Session=Depends(get_db)):
    if not db.get(Astronaut,astronaut_id): raise HTTPException(404,"Astronaut not found")
    try: return run_assessment(db,astronaut_id)
    except (ImportError,ModuleNotFoundError) as exc: raise HTTPException(503,f"ML module unavailable: {exc}")
    except ValueError as exc: raise HTTPException(422,str(exc))
