from app.models.entities import Alert
def create_risk_alerts(db, astronaut_id, assessment_id, result):
    created=[]
    indicators=result.get("indicators",{})
    for name,ind in indicators.items():
        score=ind.get("score")
        if score is None or score < 50: continue
        severity="High" if score>=75 else "Medium"
        alert=Alert(astronaut_id=astronaut_id,risk_assessment_id=assessment_id,
          title=f"{name.replace('_',' ').title()} indicator elevated",category=name.title(),
          severity=severity,status="Active",
          description=ind.get("explanation","Experimental indicator elevated."),
          recommendation="Review the underlying telemetry and follow mission medical protocols.")
        db.add(alert); created.append(alert)
    db.commit()
    return created
