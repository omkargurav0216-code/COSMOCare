from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import Astronaut,Telemetry
from app.schemas.api import TelemetryIn,TelemetryOut
router=APIRouter()
@router.post("/telemetry",response_model=TelemetryOut,status_code=201)
def create_telemetry(payload:TelemetryIn,db:Session=Depends(get_db)):
    if not db.get(Astronaut,payload.astronaut_id): raise HTTPException(404,"Astronaut not found")
    data=payload.model_dump()
    warnings=[]
    ranges={"heart_rate_bpm":(20,250),"spo2_percent":(0,100),"sleep_hours_last_24h":(0,24),"body_temperature_celsius":(25,45),"radiation_dose_rate_usv_per_hour":(0,None),"activity_level_percent":(0,100),"fatigue_level_0_10":(0,10)}
    for key,(lo,hi) in ranges.items():
        v=data.get(key)
        if v is not None and (v<lo or (hi is not None and v>hi)): warnings.append(f"unusual_{key}")
    row=Telemetry(**data,quality_warnings=warnings); db.add(row); db.commit(); db.refresh(row); return row
