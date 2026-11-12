import pandas as pd
import pytest

from ml.src.risk_assessment import calculate_risk


def make_baseline():
    return {
        "ASTRO_001": {
            "astronaut_id": "ASTRO_001",
            "metrics": {
                "heart_rate_bpm": {"mean": 80.0, "count": 48, "status": "available"},
                "spo2_percent": {"mean": 98.0, "count": 48, "status": "available"},
                "sleep_hours_last_24h": {"mean": 8.0, "count": 48, "status": "available"},
                "fatigue_level_0_10": {"mean": 3.0, "count": 48, "status": "available"},
                "activity_level_percent": {"mean": 50.0, "count": 48, "status": "available"},
            },
        }
    }


def make_history(rate=1.0):
    return pd.DataFrame({
        "astronaut_id": ["ASTRO_001", "ASTRO_001"],
        "timestamp": ["2026-11-07T10:00:00Z", "2026-11-07T11:00:00Z"],
        "radiation_dose_rate_usv_per_hour": [rate, rate],
    })


def make_telemetry():
    return {
        "astronaut_id": "ASTRO_001",
        "timestamp": "2026-11-07T12:00:00Z",
        "heart_rate_bpm": 80.0,
        "spo2_percent": 98.0,
        "sleep_hours_last_24h": 8.0,
        "fatigue_level_0_10": 0.0,
        "activity_level_percent": 50.0,
        "radiation_dose_rate_usv_per_hour": 1.0,
    }


def test_combines_all_three_indicators_with_default_weights():
    result = calculate_risk(make_telemetry(), make_baseline(), make_history())

    assert result["status"] == "available"
    assert result["available_indicator_count"] == 3
    assert result["configured_weights"] == {
        "cardiovascular": 0.40,
        "fatigue": 0.35,
        "radiation": 0.25,
    }
    assert result["effective_weights"] == {
        "cardiovascular": 0.4,
        "fatigue": 0.35,
        "radiation": 0.25,
    }
    assert result["score"] == 12.5
    assert result["category"] == "low"


def test_missing_radiation_history_renormalizes_available_weights():
    result = calculate_risk(make_telemetry(), make_baseline())

    assert result["status"] == "partially_available"
    assert result["indicators"]["radiation"]["status"] == "insufficient_data"
    assert result["effective_weights"]["cardiovascular"] == pytest.approx(0.533333, abs=1e-5)
    assert result["effective_weights"]["fatigue"] == pytest.approx(0.466667, abs=1e-5)
    assert result["effective_weights"]["radiation"] == 0.0
    assert result["score"] == 0.0
    assert "radiation_indicator_unavailable" in result["warnings"]


def test_unavailable_indicators_are_not_counted_as_zero():
    baseline = make_baseline()
    for metric in baseline["ASTRO_001"]["metrics"].values():
        metric["status"] = "insufficient_history"

    telemetry = make_telemetry()
    telemetry["fatigue_level_0_10"] = None
    result = calculate_risk(telemetry, baseline)

    assert result["score"] is None
    assert result["category"] == "insufficient_data"
    assert result["status"] == "insufficient_data"
    assert result["available_indicator_count"] == 0


def test_nested_metrics_shape_is_supported():
    telemetry = make_telemetry()
    nested = {
        "astronaut_id": telemetry["astronaut_id"],
        "timestamp": telemetry["timestamp"],
        "metrics": {
            "heart_rate_bpm": telemetry["heart_rate_bpm"],
            "spo2_percent": telemetry["spo2_percent"],
            "sleep_hours_last_24h": telemetry["sleep_hours_last_24h"],
            "fatigue_level_0_10": telemetry["fatigue_level_0_10"],
            "activity_level_percent": telemetry["activity_level_percent"],
            "radiation_dose_rate_usv_per_hour": telemetry["radiation_dose_rate_usv_per_hour"],
        },
    }

    result = calculate_risk(nested, make_baseline(), make_history())
    assert result["available_indicator_count"] == 3


def test_configurable_weights_are_applied_and_renormalized():
    result = calculate_risk(
        make_telemetry(),
        make_baseline(),
        make_history(),
        weights={
            "cardiovascular": 0.5,
            "fatigue": 0.3,
            "radiation": 0.2,
        },
    )

    assert result["configured_weights"]["cardiovascular"] == 0.5
    assert result["effective_weights"]["cardiovascular"] == 0.5


def test_rejects_negative_or_all_zero_weights():
    with pytest.raises(ValueError, match="non-negative"):
        calculate_risk(
            make_telemetry(),
            make_baseline(),
            make_history(),
            weights={"cardiovascular": -0.1},
        )

    with pytest.raises(ValueError, match="At least one"):
        calculate_risk(
            make_telemetry(),
            make_baseline(),
            make_history(),
            weights={
                "cardiovascular": 0,
                "fatigue": 0,
                "radiation": 0,
            },
        )
