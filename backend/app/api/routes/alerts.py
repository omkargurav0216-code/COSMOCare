from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import Alert,Astronaut
from app.schemas.api import AlertOut,AlertPatch
router=APIRouter()
@router.get("/alerts",response_model=list[AlertOut])
def list_alerts(status:str|None=None,db:Session=Depends(get_db)):
    q=db.query(Alert)
    if status: q=q.filter(Alert.status==status)
    return q.order_by(Alert.created_at.desc()).limit(500).all()
@router.get("/astronauts/{astronaut_id}/alerts",response_model=list[AlertOut])
def astronaut_alerts(astronaut_id:str,db:Session=Depends(get_db)):
    if not db.get(Astronaut,astronaut_id): raise HTTPException(404,"Astronaut not found")
    return db.query(Alert).filter_by(astronaut_id=astronaut_id).order_by(Alert.created_at.desc()).all()
@router.patch("/alerts/{alert_id}",response_model=AlertOut)
def update_alert(alert_id:int,payload:AlertPatch,db:Session=Depends(get_db)):
    row=db.get(Alert,alert_id)
    if not row: raise HTTPException(404,"Alert not found")
    row.status=payload.status; db.commit(); db.refresh(row); return row
