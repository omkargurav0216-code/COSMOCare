"""Tests for COSMOCare telemetry preprocessing."""

from pathlib import Path
import sys

import pandas as pd
import pytest

# Make the repository's ml/src packages importable when pytest runs from repo root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ML_SRC = PROJECT_ROOT / "ml" / "src"
if str(ML_SRC) not in sys.path:
    sys.path.insert(0, str(ML_SRC))

from preprocessing.telemetry_preprocessing import preprocess_telemetry


def valid_record(**overrides):
    record = {
        "astronaut_id": "ASTRA-01",
        "timestamp": "2026-11-11T10:00:00",
        "heart_rate_bpm": 72,
        "spo2_percent": 98,
        "sleep_hours_last_24h": 7.5,
    }
    record.update(overrides)
    return record


def test_accepts_single_record_dict():
    result = preprocess_telemetry(valid_record())
    assert len(result) == 1
    assert result.loc[0, "astronaut_id"] == "ASTRA-01"
    assert result.loc[0, "heart_rate_bpm"] == 72
    assert result.loc[0, "quality_warnings"] == ""


def test_accepts_list_of_records():
    result = preprocess_telemetry([valid_record(), valid_record(astronaut_id="ASTRA-02")])
    assert len(result) == 2
    assert result["astronaut_id"].tolist() == ["ASTRA-01", "ASTRA-02"]


def test_accepts_dataframe_and_does_not_modify_input():
    original = pd.DataFrame([valid_record(heart_rate_bpm="80")])
    before = original.copy(deep=True)

    result = preprocess_telemetry(original)

    pd.testing.assert_frame_equal(original, before)
    assert result.loc[0, "heart_rate_bpm"] == 80


def test_normalizes_naive_timestamp_to_utc():
    result = preprocess_telemetry(valid_record(timestamp="2026-11-11T10:00:00"))
    timestamp = result.loc[0, "timestamp"]
    assert str(timestamp.tz) == "UTC"


def test_converts_offset_timestamp_to_utc():
    result = preprocess_telemetry(valid_record(timestamp="2026-11-11T12:00:00+02:00"))
    assert result.loc[0, "timestamp"] == pd.Timestamp("2026-11-11T10:00:00Z")


def test_invalid_timestamp_becomes_nat_and_adds_warning():
    result = preprocess_telemetry(valid_record(timestamp="not-a-date"))
    assert pd.isna(result.loc[0, "timestamp"])
    assert "invalid_timestamp" in result.loc[0, "quality_warnings"]


@pytest.mark.parametrize(
    "column,value",
    [
        ("heart_rate_bpm", "not numeric"),
        ("heart_rate_bpm", 10),
        ("spo2_percent", 101),
        ("sleep_hours_last_24h", 25),
        ("body_temperature_celsius", 20),
        ("radiation_dose_rate_usv_per_hour", -1),
        ("activity_level_percent", 101),
        ("fatigue_level_0_10", 11),
    ],
)
def test_invalid_measurements_become_nan_with_warning(column, value):
    result = preprocess_telemetry(valid_record(**{column: value}))
    assert pd.isna(result.loc[0, column])
    assert f"invalid_{column}" in result.loc[0, "quality_warnings"]


def test_missing_measurement_stays_missing_not_zero():
    result = preprocess_telemetry(valid_record(heart_rate_bpm=None))
    assert pd.isna(result.loc[0, "heart_rate_bpm"])
    assert result.loc[0, "quality_warnings"] == ""


def test_strips_astronaut_id_whitespace():
    result = preprocess_telemetry(valid_record(astronaut_id="  ASTRA-01  "))
    assert result.loc[0, "astronaut_id"] == "ASTRA-01"


@pytest.mark.parametrize("missing_column", ["astronaut_id", "timestamp"])
def test_missing_required_column_raises_value_error(missing_column):
    record = valid_record()
    del record[missing_column]
    with pytest.raises(ValueError, match="Missing required telemetry columns"):
        preprocess_telemetry(record)


@pytest.mark.parametrize("astronaut_id", [None, "   "])
def test_missing_astronaut_id_value_raises_value_error(astronaut_id):
    with pytest.raises(ValueError, match="astronaut_id must be present"):
        preprocess_telemetry(valid_record(astronaut_id=astronaut_id))


def test_empty_dataframe_without_columns_raises_value_error():
    with pytest.raises(ValueError, match="data contains no columns"):
        preprocess_telemetry(pd.DataFrame())


@pytest.mark.parametrize("data", [None, "telemetry", 123])
def test_unsupported_input_type_raises_type_error(data):
    with pytest.raises(TypeError, match="data must be"):
        preprocess_telemetry(data)
