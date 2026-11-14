from typing import Any

from sqlalchemy.orm import Session

from app.models.entities import (
    Astronaut,
    Telemetry,
    RiskAssessment,
    Alert,
)


def _timestamp(value):
    return value.isoformat() if value else None


def build_astronaut_context(
    db: Session,
    astronaut_id: str,
) -> dict[str, Any]:

    astronaut = db.get(Astronaut, astronaut_id)

    if astronaut is None:
        raise ValueError("Astronaut not found.")

    latest_telemetry = (
        db.query(Telemetry)
        .filter(Telemetry.astronaut_id == astronaut_id)
        .order_by(Telemetry.timestamp.desc())
        .first()
    )

    latest_risk = (
        db.query(RiskAssessment)
        .filter(RiskAssessment.astronaut_id == astronaut_id)
        .order_by(RiskAssessment.created_at.desc())
        .first()
    )

    active_alerts = (
        db.query(Alert)
        .filter(
            Alert.astronaut_id == astronaut_id,
            Alert.status == "Active",
        )
        .order_by(Alert.created_at.desc())
        .limit(10)
        .all()
    )

    telemetry_data = None

    if latest_telemetry:
        telemetry_data = {
            "timestamp": _timestamp(latest_telemetry.timestamp),
            "heart_rate_bpm": latest_telemetry.heart_rate_bpm,
            "spo2_percent": latest_telemetry.spo2_percent,
            "sleep_hours_last_24h": latest_telemetry.sleep_hours_last_24h,
            "body_temperature_celsius": latest_telemetry.body_temperature_celsius,
            "radiation_dose_rate_usv_per_hour": (
                latest_telemetry.radiation_dose_rate_usv_per_hour
            ),
            "activity_level_percent": latest_telemetry.activity_level_percent,
            "fatigue_level_0_10": latest_telemetry.fatigue_level_0_10,
            "quality_warnings": latest_telemetry.quality_warnings or [],
        }

    risk_data = None

    if latest_risk:
        risk_data = {
            "score": latest_risk.score,
            "category": latest_risk.category,
            "status": latest_risk.status,
            "result": latest_risk.result,
            "created_at": _timestamp(latest_risk.created_at),
        }

    alerts_data = [
        {
            "title": alert.title,
            "category": alert.category,
            "severity": alert.severity,
            "description": alert.description,
            "recommendation": alert.recommendation,
            "status": alert.status,
            "created_at": _timestamp(alert.created_at),
        }
        for alert in active_alerts
    ]

    return {
        "astronaut": {
            "id": astronaut.id,
            "name": astronaut.name,
            "role": astronaut.role,
            "mission": astronaut.mission,
            "status": astronaut.status,
        },
        "latest_telemetry": telemetry_data,
        "latest_risk_assessment": risk_data,
        "active_alerts": alerts_data,
        "data_notes": [
            "Telemetry values are recorded observations.",
            "Risk assessments are existing machine-learning outputs.",
            "Risk scores must not be interpreted as medical diagnoses.",
            "Missing values mean the corresponding data is unavailable.",
        ],
    }
