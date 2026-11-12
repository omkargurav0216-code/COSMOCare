"""
COSMOCare telemetry preprocessing.

This module performs data-quality preparation only. It does not calculate
medical diagnoses, astronaut health risk, or NASA safety-limit violations.
Missing and invalid measurements are represented as pandas NA/NaN, never zero.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


NUMERIC_RANGES = {
    # Broad data-quality bounds for catching malformed values, not clinical limits.
    "heart_rate_bpm": (20.0, 250.0),
    "spo2_percent": (0.0, 100.0),
    "sleep_hours_last_24h": (0.0, 24.0),
    "body_temperature_celsius": (25.0, 45.0),
    "radiation_dose_rate_usv_per_hour": (0.0, None),
    "activity_level_percent": (0.0, 100.0),
    "fatigue_level_0_10": (0.0, 10.0),
}

REQUIRED_COLUMNS = ("astronaut_id", "timestamp")


def _to_dataframe(data: Any) -> pd.DataFrame:
    """Accept a DataFrame, one telemetry record, or a list of records."""
    if isinstance(data, pd.DataFrame):
        return data.copy()
    if isinstance(data, dict):
        return pd.DataFrame([data])
    if isinstance(data, list):
        return pd.DataFrame(data)
    raise TypeError(
        "data must be a pandas DataFrame, a telemetry-record dict, "
        "or a list of telemetry-record dicts"
    )


def preprocess_telemetry(data: Any) -> pd.DataFrame:
    """
    Validate and normalize telemetry records.

    Behaviour:
    - preserves the input columns and rows;
    - requires astronaut_id and timestamp columns;
    - normalizes timestamps to UTC (invalid timestamps become NaT);
    - converts known measurements to numeric values;
    - sets malformed/out-of-bounds measurements to NaN, not zero;
    - adds `quality_warnings`, a semicolon-separated explanation per row;
    - does not impute missing values or apply clinical thresholds.

    Returns a new DataFrame; the input object is not modified.
    """
    frame = _to_dataframe(data)

    if frame.empty and len(frame.columns) == 0:
        raise ValueError("data contains no columns")

    missing_required = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing_required:
        raise ValueError(
            "Missing required telemetry columns: " + ", ".join(missing_required)
        )

    warnings: list[list[str]] = [[] for _ in range(len(frame))]

    # Normalize IDs without inventing an ID for missing records.
    frame["astronaut_id"] = frame["astronaut_id"].astype("string").str.strip()
    missing_ids = frame["astronaut_id"].isna() | frame["astronaut_id"].eq("")
    for position in missing_ids[missing_ids].index:
        warnings[frame.index.get_loc(position)].append("missing_astronaut_id")
    if missing_ids.any():
        raise ValueError("astronaut_id must be present for every telemetry record")

    # utc=True makes naive timestamps UTC and converts offset-aware timestamps to UTC.
    parsed_timestamps = pd.to_datetime(frame["timestamp"], errors="coerce", utc=True)
    invalid_timestamp = parsed_timestamps.isna()
    for position in invalid_timestamp[invalid_timestamp].index:
        warnings[frame.index.get_loc(position)].append("invalid_timestamp")
    frame["timestamp"] = parsed_timestamps

    for column, (lower, upper) in NUMERIC_RANGES.items():
        if column not in frame.columns:
            continue

        original = frame[column]
        numeric = pd.to_numeric(original, errors="coerce")

        malformed = original.notna() & numeric.isna()
        out_of_range = pd.Series(False, index=frame.index)
        if lower is not None:
            out_of_range |= numeric.notna() & (numeric < lower)
        if upper is not None:
            out_of_range |= numeric.notna() & (numeric > upper)

        invalid = malformed | out_of_range
        for position in invalid[invalid].index:
            warnings[frame.index.get_loc(position)].append(f"invalid_{column}")

        # Do not replace missing or invalid measurements with zero.
        frame[column] = numeric.mask(invalid)

    # A stable, readable warning field makes data-quality issues inspectable downstream.
    frame["quality_warnings"] = [
        ";".join(row_warnings) for row_warnings in warnings
    ]

    return frame.reset_index(drop=True)
