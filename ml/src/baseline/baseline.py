"""
Astronaut-specific historical baseline calculation for COSMOCare.

Baselines describe an individual's observed history. They are not medical
reference ranges, diagnostic thresholds, or NASA safety limits.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


BASELINE_METRICS = (
    "heart_rate_bpm",
    "spo2_percent",
    "sleep_hours_last_24h",
    "body_temperature_celsius",
    "radiation_dose_rate_usv_per_hour",
    "activity_level_percent",
    "fatigue_level_0_10",
)


def calculate_baseline(
    history: Any,
    min_history: int = 24,
) -> dict[str, dict[str, Any]]:
    """
    Calculate per-astronaut, per-metric historical baselines.

    Parameters
    ----------
    history:
        A pandas DataFrame or list of telemetry dictionaries. Must contain
        `astronaut_id`; recognized measurement columns are summarized when
        present.
    min_history:
        Minimum number of valid, non-missing observations required for a
        metric to receive status `available`. Defaults to 24 readings
        (one day of hourly sample data). This is a prototype data sufficiency
        setting, not a medical standard.

    Returns
    -------
    dict:
        Mapping of astronaut_id to a result containing each metric's count,
        mean, median, standard deviation, minimum, maximum, and status.
        Metrics with too few valid observations have status
        `insufficient_history`; summary statistics are still provided when
        at least one valid observation exists. No missing values are filled.
    """
    if not isinstance(min_history, int) or min_history < 1:
        raise ValueError("min_history must be a positive integer")

    if isinstance(history, pd.DataFrame):
        frame = history.copy()
    elif isinstance(history, list):
        frame = pd.DataFrame(history)
    elif isinstance(history, dict):
        frame = pd.DataFrame([history])
    else:
        raise TypeError(
            "history must be a pandas DataFrame, a record dictionary, "
            "or a list of record dictionaries"
        )

    if "astronaut_id" not in frame.columns:
        raise ValueError("history must contain an astronaut_id column")

    ids = frame["astronaut_id"].astype("string").str.strip()
    if ids.isna().any() or ids.eq("").any():
        raise ValueError("astronaut_id must be present for every history record")

    available_metrics = [m for m in BASELINE_METRICS if m in frame.columns]
    if not available_metrics:
        raise ValueError("history contains no recognized telemetry metric columns")

    frame["astronaut_id"] = ids
    for metric in available_metrics:
        frame[metric] = pd.to_numeric(frame[metric], errors="coerce")

    result: dict[str, dict[str, Any]] = {}

    for astronaut_id, astronaut_frame in frame.groupby("astronaut_id", sort=True):
        metric_results: dict[str, Any] = {}

        for metric in available_metrics:
            values = astronaut_frame[metric].dropna()
            count = int(values.count())

            if count == 0:
                stats = {
                    "count": 0,
                    "mean": None,
                    "median": None,
                    "std": None,
                    "min": None,
                    "max": None,
                    "status": "insufficient_history",
                }
            else:
                stats = {
                    "count": count,
                    "mean": float(values.mean()),
                    "median": float(values.median()),
                    "std": float(values.std(ddof=1)) if count > 1 else None,
                    "min": float(values.min()),
                    "max": float(values.max()),
                    "status": (
                        "available" if count >= min_history
                        else "insufficient_history"
                    ),
                }

            metric_results[metric] = stats

        result[str(astronaut_id)] = {
            "astronaut_id": str(astronaut_id),
            "history_records": int(len(astronaut_frame)),
            "minimum_required_observations": min_history,
            "metrics": metric_results,
        }

    return result
