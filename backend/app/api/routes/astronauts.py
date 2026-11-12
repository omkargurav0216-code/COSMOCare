from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import Astronaut,Telemetry
from app.schemas.api import AstronautOut,TelemetryOut
router=APIRouter()
@router.get("/astronauts",response_model=list[AstronautOut])
def list_astronauts(db:Session=Depends(get_db)): return db.query(Astronaut).order_by(Astronaut.id).all()
@router.get("/astronauts/{astronaut_id}",response_model=AstronautOut)
def get_astronaut(astronaut_id:str,db:Session=Depends(get_db)):
    item=db.get(Astronaut,astronaut_id)
    if not item: raise HTTPException(404,"Astronaut not found")
    return item
@router.get("/astronauts/{astronaut_id}/telemetry",response_model=list[TelemetryOut])
def astronaut_telemetry(astronaut_id:str,limit:int=100,db:Session=Depends(get_db)):
    if not db.get(Astronaut,astronaut_id): raise HTTPException(404,"Astronaut not found")
    return db.query(Telemetry).filter_by(astronaut_id=astronaut_id).order_by(Telemetry.timestamp.desc()).limit(min(max(limit,1),1000)).all()
