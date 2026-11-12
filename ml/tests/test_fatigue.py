import pytest

from ml.src.risk_assessment.fatigue import calculate_fatigue_risk


def make_baseline(sleep=8.0, fatigue=3.0, activity=50.0, status="available"):
    return {
        "ASTRO_001": {
            "astronaut_id": "ASTRO_001",
            "metrics": {
                "sleep_hours_last_24h": {"mean": sleep, "count": 48, "status": status},
                "fatigue_level_0_10": {"mean": fatigue, "count": 48, "status": status},
                "activity_level_percent": {"mean": activity, "count": 48, "status": status},
            },
        }
    }


def test_sleep_at_baseline_and_zero_fatigue_produce_zero_score():
    result = calculate_fatigue_risk(
        {
            "astronaut_id": "ASTRO_001",
            "sleep_hours_last_24h": 8,
            "fatigue_level_0_10": 0,
        },
        make_baseline(),
    )

    assert result["score"] == 0.0
    assert result["category"] == "low"
    assert result["status"] == "available"


def test_sleep_deficit_and_self_report_contribute_to_score():
    result = calculate_fatigue_risk(
        {
            "astronaut_id": "ASTRO_001",
            "sleep_hours_last_24h": 6,
            "fatigue_level_0_10": 8,
            "activity_level_percent": 40,
        },
        make_baseline(),
    )

    assert result["components"]["sleep_hours_last_24h"]["score"] == 100.0
    assert result["components"]["fatigue_level_0_10"]["score"] == 80.0
    assert result["score"] == 92.0
    assert result["category"] == "high"


def test_activity_is_context_only_and_not_scored():
    result = calculate_fatigue_risk(
        {
            "astronaut_id": "ASTRO_001",
            "sleep_hours_last_24h": 8,
            "fatigue_level_0_10": 0,
            "activity_level_percent": 95,
        },
        make_baseline(),
    )

    assert result["context"]["activity_level_percent"]["used_in_score"] is False
    assert result["score"] == 0.0


def test_missing_sleep_baseline_does_not_prevent_fatigue_component():
    result = calculate_fatigue_risk(
        {
            "astronaut_id": "ASTRO_001",
            "sleep_hours_last_24h": 6,
            "fatigue_level_0_10": 5,
        },
        make_baseline(status="insufficient_history"),
    )

    assert result["components"]["sleep_hours_last_24h"]["status"] == "unavailable"
    assert result["components"]["fatigue_level_0_10"]["status"] == "available"
    assert result["score"] == 50.0
    assert "insufficient_baseline_sleep_hours_last_24h" in result["warnings"]


def test_no_usable_inputs_returns_insufficient_data():
    result = calculate_fatigue_risk(
        {"astronaut_id": "ASTRO_001"},
        make_baseline(status="insufficient_history"),
    )

    assert result["score"] is None
    assert result["category"] == "insufficient_data"
    assert result["status"] == "insufficient_data"


def test_supports_nested_metrics_input():
    result = calculate_fatigue_risk(
        {
            "astronaut_id": "ASTRO_001",
            "metrics": {
                "sleep_hours_last_24h": 8,
                "fatigue_level_0_10": 0,
            },
        },
        make_baseline(),
    )

    assert result["score"] == 0.0


def test_rejects_non_positive_sleep_threshold():
    with pytest.raises(ValueError, match="positive number"):
        calculate_fatigue_risk(
            {"astronaut_id": "ASTRO_001", "fatigue_level_0_10": 5},
            make_baseline(),
            thresholds={"sleep_deficit_hours_for_full_score": 0},
        )
