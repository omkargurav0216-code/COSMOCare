from datetime import datetime, timedelta, timezone
from app.models.entities import Astronaut,Telemetry
def seed_database(db):
    if db.query(Astronaut).count(): return
    people=[
      ("AST-001","Alex Morgan","Mission Commander",42,72,98,7.5,36.8,.42,2),
      ("AST-002","Sarah Chen","Flight Engineer",36,88,96,5.8,37.1,.51,5),
      ("AST-003","James Wilson","Medical Officer",39,68,99,8.0,36.6,.38,1),
      ("AST-004","Elena Rodriguez","Research Specialist",34,75,98,7.2,36.9,.45,2)]
    now=datetime.now(timezone.utc)
    for aid,name,role,age,hr,spo,sleep,temp,rad,fatigue in people:
        db.add(Astronaut(id=aid,name=name,role=role,age=age,mission="ASTRA-01",status="Active"))
        for i in range(30):
            db.add(Telemetry(astronaut_id=aid,timestamp=now-timedelta(hours=29-i),
              heart_rate_bpm=hr+(i%5-2),spo2_percent=spo,sleep_hours_last_24h=sleep,
              body_temperature_celsius=temp,radiation_dose_rate_usv_per_hour=rad+(i%3)*.01,
              activity_level_percent=45+(i%10),fatigue_level_0_10=fatigue,
              quality_warnings=[]))
    db.commit()
