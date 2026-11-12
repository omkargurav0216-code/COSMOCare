import pandas as pd
import pytest

from ml.src.risk_assessment.radiation import calculate_radiation_risk


def make_history():
    return pd.DataFrame({
        "astronaut_id": ["ASTRO_001", "ASTRO_001", "ASTRO_001"],
        "timestamp": [
            "2026-11-07T10:00:00Z",
            "2026-11-07T11:00:00Z",
            "2026-11-07T12:00:00Z",
        ],
        "radiation_dose_rate_usv_per_hour": [1.0, 1.0, 1.0],
    })


def current(rate=1.0, timestamp="2026-11-07T13:00:00Z"):
    return {
        "astronaut_id": "ASTRO_001",
        "timestamp": timestamp,
        "radiation_dose_rate_usv_per_hour": rate,
    }


def test_integrates_constant_rate_over_observed_hours():
    result = calculate_radiation_risk(current(1.0), make_history())

    # Three adjacent one-hour intervals at 1 µSv/hour.
    assert result["accumulated_dose_usv"] == 3.0
    assert result["integrated_intervals"] == 3
    assert result["skipped_time_gaps"] == 0


def test_trapezoidal_integration_for_changing_rate():
    history = pd.DataFrame({
        "astronaut_id": ["ASTRO_001", "ASTRO_001"],
        "timestamp": ["2026-11-07T10:00:00Z", "2026-11-07T11:00:00Z"],
        "radiation_dose_rate_usv_per_hour": [1.0, 3.0],
    })
    result = calculate_radiation_risk(
        current(3.0, "2026-11-07T12:00:00Z"),
        history,
    )

    # (1+3)/2 * 1h + (3+3)/2 * 1h = 5 µSv
    assert result["accumulated_dose_usv"] == 5.0


def test_rate_indicator_compares_current_rate_to_personal_history():
    result = calculate_radiation_risk(current(2.0), make_history())

    assert result["rate_component"]["current_to_historical_ratio"] == 2.0
    assert result["score"] == 100.0
    assert result["category"] == "high"


def test_other_astronaut_history_is_not_used():
    history = pd.DataFrame({
        "astronaut_id": ["ASTRO_002", "ASTRO_002"],
        "timestamp": ["2026-11-07T10:00:00Z", "2026-11-07T11:00:00Z"],
        "radiation_dose_rate_usv_per_hour": [1.0, 1.0],
    })
    result = calculate_radiation_risk(current(2.0), history)

    assert result["historical_mean_dose_rate_usv_per_hour"] is None
    assert result["score"] is None
    assert result["category"] == "insufficient_data"


def test_long_gaps_are_skipped_not_extrapolated():
    history = pd.DataFrame({
        "astronaut_id": ["ASTRO_001", "ASTRO_001"],
        "timestamp": ["2026-11-07T00:00:00Z", "2026-11-07T08:00:00Z"],
        "radiation_dose_rate_usv_per_hour": [1.0, 1.0],
    })
    result = calculate_radiation_risk(
        current(1.0, "2026-11-07T09:00:00Z"),
        history,
        max_gap_hours=2,
    )

    assert result["accumulated_dose_usv"] == 1.0
    assert result["integrated_intervals"] == 1
    assert result["skipped_time_gaps"] == 1
    assert "one_or_more_time_gaps_skipped" in result["warnings"]


def test_missing_current_rate_does_not_become_zero():
    result = calculate_radiation_risk(current(None), make_history())

    assert result["current_dose_rate_usv_per_hour"] is None
    assert result["score"] is None
    assert "missing_or_invalid_radiation_dose_rate_usv_per_hour" in result["warnings"]


def test_supports_nested_metrics_shape():
    nested = {
        "astronaut_id": "ASTRO_001",
        "timestamp": "2026-11-07T13:00:00Z",
        "metrics": {"radiation_dose_rate_usv_per_hour": 1.0},
    }
    result = calculate_radiation_risk(nested, make_history())

    assert result["current_dose_rate_usv_per_hour"] == 1.0
    assert result["score"] == 50.0


def test_rejects_invalid_gap_and_threshold():
    with pytest.raises(ValueError, match="max_gap_hours"):
        calculate_radiation_risk(current(), make_history(), max_gap_hours=0)

    with pytest.raises(ValueError, match="greater than 1"):
        calculate_radiation_risk(
            current(),
            make_history(),
            thresholds={"rate_ratio_for_full_score": 1},
        )
