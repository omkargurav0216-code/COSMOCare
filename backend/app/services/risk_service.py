from app.models.entities import Telemetry, RiskAssessment
from app.ml import analyze
from app.services.alert_service import create_risk_alerts

def run_assessment(db, astronaut_id, current=None):
    history = db.query(Telemetry).filter(Telemetry.astronaut_id == astronaut_id).order_by(Telemetry.timestamp.asc()).all()
    if not history:
        raise ValueError("No telemetry history available")
    current = current or history[-1]
    result = analyze(current, history[:-1] if len(history) > 1 else history)
    row = RiskAssessment(
        astronaut_id=astronaut_id,
        telemetry_id=current.id,
        score=result.get("score"),
        category=result.get("category", "insufficient_data"),
        status=result.get("status", "insufficient_data"),
        result=result,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    create_risk_alerts(db, astronaut_id, row.id, result)
    return row
