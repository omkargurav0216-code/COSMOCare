import pandas as pd
import pytest
from ml.src.anomaly_detection.model_loader import load_anomaly_model, predict_anomaly


def test_missing_artifact_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_anomaly_model(tmp_path / "missing.joblib")


def test_load_and_predict_persisted_model():
    artifact = load_anomaly_model()
    result = predict_anomaly({
        "heart_rate_bpm": 80, "spo2_percent": 97,
        "sleep_hours_last_24h": 7, "body_temperature_celsius": 36.8,
        "radiation_dose_rate_usv_per_hour": 0.3,
        "activity_level_percent": 60, "fatigue_level_0_10": 4,
    }, artifact)
    assert result["status"] == "available"
    assert isinstance(result["is_anomaly"], bool)
    assert result["model_version"] == "1.1.0"


def test_prediction_requires_one_record():
    artifact = load_anomaly_model()
    with pytest.raises(ValueError, match="exactly one"):
        predict_anomaly(pd.DataFrame([{}, {}]), artifact)
