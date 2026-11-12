import pandas as pd
import pytest

from ml.src.baseline.baseline import calculate_baseline


def test_calculates_individual_baseline_statistics():
    history = pd.DataFrame({
        "astronaut_id": ["ASTRO_001"] * 3,
        "heart_rate_bpm": [70, 80, 90],
        "spo2_percent": [98, 97, 99],
    })

    result = calculate_baseline(history, min_history=3)
    hr = result["ASTRO_001"]["metrics"]["heart_rate_bpm"]

    assert hr["count"] == 3
    assert hr["mean"] == 80.0
    assert hr["median"] == 80.0
    assert hr["min"] == 70.0
    assert hr["max"] == 90.0
    assert hr["status"] == "available"


def test_calculates_separate_baselines_for_each_astronaut():
    history = [
        {"astronaut_id": "ASTRO_001", "heart_rate_bpm": 70},
        {"astronaut_id": "ASTRO_001", "heart_rate_bpm": 80},
        {"astronaut_id": "ASTRO_002", "heart_rate_bpm": 100},
        {"astronaut_id": "ASTRO_002", "heart_rate_bpm": 110},
    ]

    result = calculate_baseline(history, min_history=2)

    assert result["ASTRO_001"]["metrics"]["heart_rate_bpm"]["median"] == 75.0
    assert result["ASTRO_002"]["metrics"]["heart_rate_bpm"]["median"] == 105.0


def test_insufficient_history_is_explicit():
    history = [{
        "astronaut_id": "ASTRO_001",
        "heart_rate_bpm": 80,
    }]

    result = calculate_baseline(history, min_history=24)
    hr = result["ASTRO_001"]["metrics"]["heart_rate_bpm"]

    assert hr["count"] == 1
    assert hr["status"] == "insufficient_history"
    assert hr["median"] == 80.0


def test_missing_values_are_not_replaced_with_zero():
    history = [
        {"astronaut_id": "ASTRO_001", "heart_rate_bpm": None},
        {"astronaut_id": "ASTRO_001", "heart_rate_bpm": 80},
    ]

    result = calculate_baseline(history, min_history=2)
    hr = result["ASTRO_001"]["metrics"]["heart_rate_bpm"]

    assert hr["count"] == 1
    assert hr["mean"] == 80.0
    assert hr["status"] == "insufficient_history"


def test_rejects_missing_astronaut_id_column():
    with pytest.raises(ValueError, match="astronaut_id"):
        calculate_baseline([{"heart_rate_bpm": 80}])


def test_rejects_invalid_minimum_history():
    with pytest.raises(ValueError, match="positive integer"):
        calculate_baseline(
            [{"astronaut_id": "ASTRO_001", "heart_rate_bpm": 80}],
            min_history=0,
        )
