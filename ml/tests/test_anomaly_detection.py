import numpy as np
import pandas as pd
import pytest

from ml.src.anomaly_detection import detect_anomalies


def make_history(rows=40, astronaut_id="ASTRO_001"):
    rng = np.random.default_rng(7)
    return pd.DataFrame({
        "astronaut_id": [astronaut_id] * rows,
        "timestamp": pd.date_range("2026-01-01", periods=rows, freq="h", tz="UTC"),
        "heart_rate_bpm": rng.normal(70, 2, rows),
        "spo2_percent": rng.normal(98, 0.5, rows),
        "sleep_hours_last_24h": rng.normal(7.5, 0.3, rows),
    })


def test_returns_available_result_for_valid_history():
    result = detect_anomalies(make_history(), {
        "astronaut_id": "ASTRO_001", "heart_rate_bpm": 71,
        "spo2_percent": 98, "sleep_hours_last_24h": 7.4,
    })
    assert result["status"] == "available"
    assert isinstance(result["is_anomaly"], bool)
    assert isinstance(result["anomaly_score"], float)
    assert result["historical_sample_count"] == 40


def test_large_deviation_is_flagged_as_anomaly():
    result = detect_anomalies(make_history(), {
        "astronaut_id": "ASTRO_001", "heart_rate_bpm": 150,
        "spo2_percent": 80, "sleep_hours_last_24h": 1,
    })
    assert result["status"] == "available"
    assert result["is_anomaly"] is True


def test_uses_only_matching_astronaut_history():
    history = pd.concat([make_history(30, "ASTRO_001"),
                         make_history(30, "ASTRO_002")], ignore_index=True)
    result = detect_anomalies(history, {
        "astronaut_id": "ASTRO_001", "heart_rate_bpm": 70,
        "spo2_percent": 98, "sleep_hours_last_24h": 7.5,
    })
    assert result["historical_sample_count"] == 30


def test_insufficient_history_returns_explicit_status():
    result = detect_anomalies(make_history(10), {
        "astronaut_id": "ASTRO_001", "heart_rate_bpm": 70,
        "spo2_percent": 98, "sleep_hours_last_24h": 7.5,
    })
    assert result["status"] == "insufficient_data"
    assert result["is_anomaly"] is None
    assert result["anomaly_score"] is None


def test_missing_current_values_are_not_imputed_to_zero():
    result = detect_anomalies(make_history(), {
        "astronaut_id": "ASTRO_001", "heart_rate_bpm": None,
        "spo2_percent": None, "sleep_hours_last_24h": None,
    })
    assert result["status"] == "insufficient_data"
    assert result["is_anomaly"] is None


def test_drops_incomplete_historical_rows():
    history = make_history()
    history.loc[0:4, "heart_rate_bpm"] = np.nan
    result = detect_anomalies(history, {
        "astronaut_id": "ASTRO_001", "heart_rate_bpm": 70,
        "spo2_percent": 98, "sleep_hours_last_24h": 7.5,
    })
    assert result["status"] == "available"
    assert result["historical_sample_count"] == 35


def test_rejects_multiple_current_records():
    with pytest.raises(ValueError, match="exactly one"):
        detect_anomalies(make_history(), [{"heart_rate_bpm": 70}, {"heart_rate_bpm": 71}])


@pytest.mark.parametrize("value", [0, 1, 2.5, True])
def test_rejects_invalid_min_history(value):
    with pytest.raises(ValueError):
        detect_anomalies(make_history(), {"heart_rate_bpm": 70}, min_history=value)


@pytest.mark.parametrize("value", [0, -0.1, 0.6, "invalid"])
def test_rejects_invalid_contamination(value):
    with pytest.raises(ValueError):
        detect_anomalies(make_history(), {
            "heart_rate_bpm": 70, "spo2_percent": 98, "sleep_hours_last_24h": 7.5,
        }, contamination=value)


def test_rejects_invalid_estimator_count():
    with pytest.raises(ValueError):
        detect_anomalies(make_history(), {
            "heart_rate_bpm": 70, "spo2_percent": 98, "sleep_hours_last_24h": 7.5,
        }, n_estimators=0)
