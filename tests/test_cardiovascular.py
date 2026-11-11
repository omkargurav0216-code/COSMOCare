import pytest

from ml.src.risk_assessment.cardiovascular import calculate_cardiovascular_risk


def make_baseline(hr=80.0, spo2=98.0, status="available"):
    return {
        "ASTRO_001": {
            "astronaut_id": "ASTRO_001",
            "metrics": {
                "heart_rate_bpm": {"mean": hr, "count": 48, "status": status},
                "spo2_percent": {"mean": spo2, "count": 48, "status": status},
            },
        }
    }


def test_baseline_like_values_produce_low_indicator():
    result = calculate_cardiovascular_risk(
        {"astronaut_id": "ASTRO_001", "heart_rate_bpm": 80, "spo2_percent": 98},
        make_baseline(),
    )

    assert result["score"] == 0.0
    assert result["category"] == "low"
    assert result["status"] == "available"


def test_deviations_increase_component_scores():
    result = calculate_cardiovascular_risk(
        {"astronaut_id": "ASTRO_001", "heart_rate_bpm": 96, "spo2_percent": 94},
        make_baseline(),
    )

    assert result["components"]["heart_rate_bpm"]["score"] == 100.0
    assert result["components"]["spo2_percent"]["score"] == 100.0
    assert result["score"] == 100.0
    assert result["category"] == "high"


def test_missing_metric_is_not_treated_as_zero():
    result = calculate_cardiovascular_risk(
        {"astronaut_id": "ASTRO_001", "heart_rate_bpm": 80},
        make_baseline(),
    )

    assert result["components"]["spo2_percent"]["status"] == "unavailable"
    assert result["score"] == 0.0
    assert "missing_or_invalid_spo2_percent" in result["warnings"]


def test_insufficient_baseline_produces_insufficient_data_when_all_missing():
    result = calculate_cardiovascular_risk(
        {"astronaut_id": "ASTRO_001", "heart_rate_bpm": 80, "spo2_percent": 98},
        make_baseline(status="insufficient_history"),
    )

    assert result["score"] is None
    assert result["category"] == "insufficient_data"
    assert result["status"] == "insufficient_data"


def test_supports_nested_shared_metrics_shape():
    result = calculate_cardiovascular_risk(
        {
            "astronaut_id": "ASTRO_001",
            "metrics": {"heart_rate_bpm": 80, "spo2_percent": 98},
        },
        make_baseline(),
    )

    assert result["score"] == 0.0


def test_rejects_non_positive_threshold():
    with pytest.raises(ValueError, match="positive number"):
        calculate_cardiovascular_risk(
            {"astronaut_id": "ASTRO_001", "heart_rate_bpm": 80, "spo2_percent": 98},
            make_baseline(),
            thresholds={"spo2_drop_percentage_points": 0},
        )
