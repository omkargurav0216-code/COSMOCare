from datetime import datetime, timezone
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator
class AstronautOut(BaseModel):
    id:str; name:str; role:str; mission:str; age:Optional[int]=None; status:str
    model_config=ConfigDict(from_attributes=True)
class TelemetryIn(BaseModel):
    astronaut_id:str=Field(min_length=1,max_length=64)
    timestamp:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
    heart_rate_bpm:Optional[float]=Field(None,ge=0,le=300)
    spo2_percent:Optional[float]=Field(None,ge=0,le=100)
    sleep_hours_last_24h:Optional[float]=Field(None,ge=0,le=24)
    body_temperature_celsius:Optional[float]=Field(None,ge=25,le=45)
    radiation_dose_rate_usv_per_hour:Optional[float]=Field(None,ge=0)
    activity_level_percent:Optional[float]=Field(None,ge=0,le=100)
    fatigue_level_0_10:Optional[float]=Field(None,ge=0,le=10)
    @field_validator("timestamp")
    @classmethod
    def timestamp_aware(cls,v):
        return v.replace(tzinfo=timezone.utc) if v.tzinfo is None else v
class TelemetryOut(TelemetryIn):
    id:int
    quality_warnings:list[str]=[]
    model_config=ConfigDict(from_attributes=True)
class RiskOut(BaseModel):
    id:int; astronaut_id:str; score:Optional[float]; category:str; status:str; result:dict[str,Any]; created_at:datetime
    model_config=ConfigDict(from_attributes=True)
class AlertOut(BaseModel):
    id:int; astronaut_id:str; title:str; category:str; severity:str; description:str; recommendation:str; status:str; created_at:datetime
    model_config=ConfigDict(from_attributes=True)
class AlertPatch(BaseModel):
    status:str=Field(pattern="^(Active|Acknowledged|Resolved)$")
class SimulationIn(BaseModel):
    astronaut_id:str
    metrics:dict[str,float]
class ChatIn(BaseModel):
    astronaut_id:Optional[str]=None
    conversation_id:Optional[str]=None
    message:str=Field(min_length=1,max_length=10000)
class ChatOut(BaseModel):
    conversation_id:str
    status:str="integration_pending"
    message:str
