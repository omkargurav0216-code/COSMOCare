from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON, Index
from sqlalchemy.orm import relationship
from app.database.session import Base
def utcnow(): return datetime.now(timezone.utc)
class Astronaut(Base):
    __tablename__="astronauts"
    id=Column(String,primary_key=True,index=True)
    name=Column(String,nullable=False)
    role=Column(String,default="Crew Member")
    mission=Column(String,default="ASTRA-01")
    age=Column(Integer,nullable=True)
    status=Column(String,default="Active")
    created_at=Column(DateTime(timezone=True),default=utcnow)
    telemetry=relationship("Telemetry",back_populates="astronaut",cascade="all, delete-orphan")
class Telemetry(Base):
    __tablename__="telemetry"
    id=Column(Integer,primary_key=True,index=True)
    astronaut_id=Column(String,ForeignKey("astronauts.id"),nullable=False,index=True)
    timestamp=Column(DateTime(timezone=True),nullable=False,index=True)
    heart_rate_bpm=Column(Float)
    spo2_percent=Column(Float)
    sleep_hours_last_24h=Column(Float)
    body_temperature_celsius=Column(Float)
    radiation_dose_rate_usv_per_hour=Column(Float)
    activity_level_percent=Column(Float)
    fatigue_level_0_10=Column(Float)
    quality_warnings=Column(JSON,default=list)
    astronaut=relationship("Astronaut",back_populates="telemetry")
    __table_args__=(Index("ix_telemetry_astronaut_timestamp","astronaut_id","timestamp"),)
class RiskAssessment(Base):
    __tablename__="risk_assessments"
    id=Column(Integer,primary_key=True,index=True)
    astronaut_id=Column(String,ForeignKey("astronauts.id"),nullable=False,index=True)
    telemetry_id=Column(Integer,ForeignKey("telemetry.id"),nullable=True)
    score=Column(Float)
    category=Column(String,nullable=False)
    status=Column(String,nullable=False)
    result=Column(JSON,nullable=False)
    created_at=Column(DateTime(timezone=True),default=utcnow)
class Alert(Base):
    __tablename__="alerts"
    id=Column(Integer,primary_key=True,index=True)
    astronaut_id=Column(String,ForeignKey("astronauts.id"),nullable=False,index=True)
    risk_assessment_id=Column(Integer,ForeignKey("risk_assessments.id"),nullable=True)
    title=Column(String,nullable=False)
    category=Column(String,default="General")
    severity=Column(String,default="Low")
    description=Column(Text,default="")
    recommendation=Column(Text,default="")
    status=Column(String,default="Active")
    created_at=Column(DateTime(timezone=True),default=utcnow)
    updated_at=Column(DateTime(timezone=True),default=utcnow,onupdate=utcnow)
class Conversation(Base):
    __tablename__="conversations"
    id=Column(String,primary_key=True)
    astronaut_id=Column(String,ForeignKey("astronauts.id"),nullable=True,index=True)
    provider_conversation_id=Column(String,nullable=True)
    created_at=Column(DateTime(timezone=True),default=utcnow)
class Message(Base):
    __tablename__="messages"
    id=Column(Integer,primary_key=True)
    conversation_id=Column(String,ForeignKey("conversations.id"),nullable=False,index=True)
    role=Column(String,nullable=False)
    content=Column(Text,nullable=False)
    created_at=Column(DateTime(timezone=True),default=utcnow)
