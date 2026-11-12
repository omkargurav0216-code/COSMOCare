"""
Prototype radiation exposure indicator for COSMOCare.

Radiation input is a dose rate in µSv/hour. This module estimates accumulated
dose over observed intervals; it does not apply NASA exposure limits or make
medical/safety determinations.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


DEFAULT_THRESHOLDS = {
    # A current dose rate 2x the personal historical mean maps to 100 points.
    # This is a demo comparison setting, not a radiation safety threshold.
    "rate_ratio_for_full_score": 2.0,
}


def _to_frame(data: Any, label: str) -> pd.DataFrame:
    if isinstance(data, pd.DataFrame):
        return data.copy()
    if isinstance(data, dict):
        return pd.DataFrame([data])
    if isinstance(data, list):
        return pd.DataFrame(data)
    raise TypeError(
        f"{label} must be a pandas DataFrame, a record dictionary, "
        "or a list of record dictionaries"
    )


def _extract_current(data: dict[str, Any]) -> dict[str, Any]:
    nested = data.get("metrics")
    if isinstance(nested, dict):
        return {**data, **nested}
    return data


def _valid_rate(value: Any) -> float | None:
    try:
        rate = float(value)
    except (TypeError, ValueError):
        return None
    if rate != rate or abs(rate) == float("inf") or rate < 0:
        return None
    return rate


def _integrate_observed_dose(
    records: pd.DataFrame,
    max_gap_hours: float,
) -> tuple[float, int, int]:
    """
    Trapezoidal integration of dose rate over valid adjacent observations.

    Intervals larger than max_gap_hours are skipped rather than assuming
    continuous exposure during an unobserved gap.
    """
    if records.empty:
        return 0.0, 0, 0

    frame = records.copy()
    frame["timestamp"] = pd.to_datetime(
        frame["timestamp"], errors="coerce", utc=True
    )
    frame["radiation_dose_rate_usv_per_hour"] = pd.to_numeric(
        frame["radiation_dose_rate_usv_per_hour"], errors="coerce"
    )
    frame = frame.dropna(
        subset=["timestamp", "radiation_dose_rate_usv_per_hour"]
    )
    frame = frame[
        frame["radiation_dose_rate_usv_per_hour"].ge(0)
    ]
    frame = frame.sort_values("timestamp").drop_duplicates(
        subset=["timestamp"], keep="last"
    )

    total_dose = 0.0
    integrated_intervals = 0
    skipped_gaps = 0

    rows = list(
        frame[["timestamp", "radiation_dose_rate_usv_per_hour"]]
        .itertuples(index=False, name=None)
    )

    for (time_a, rate_a), (time_b, rate_b) in zip(rows, rows[1:]):
        hours = (time_b - time_a).total_seconds() / 3600.0
        if hours <= 0:
            continue
        if hours > max_gap_hours:
            skipped_gaps += 1
            continue
        total_dose += ((float(rate_a) + float(rate_b)) / 2.0) * hours
        integrated_intervals += 1

    return round(total_dose, 6), integrated_intervals, skipped_gaps


def calculate_radiation_risk(
    telemetry: dict[str, Any],
    history: Any,
    thresholds: dict[str, float] | None = None,
    max_gap_hours: float = 2.0,
) -> dict[str, Any]:
    """
    Estimate observed accumulated dose and an experimental dose-rate indicator.

    Parameters
    ----------
    telemetry:
        Current record with astronaut_id, timestamp, and
        radiation_dose_rate_usv_per_hour. A nested `metrics` object is also
        accepted.
    history:
        Historical records for the same astronaut. May be a DataFrame, list
        of dictionaries, or a single dictionary.
    thresholds:
        Optional configuration. `rate_ratio_for_full_score` defaults to 2.0.
        It means a current rate 2x the historical mean maps to 100 component
        points; it is not an exposure safety limit.
    max_gap_hours:
        Maximum interval over which dose rate is integrated. Larger gaps are
        skipped and counted, because exposure during missing time is unknown.

    Returns
    -------
    dict:
        `accumulated_dose_usv` is the trapezoidal estimate over valid observed
        intervals in history plus the current record. It is not lifetime dose.
        The 0–100 indicator compares current dose rate with the historical
        mean for that astronaut. A score/category is withheld when the
        historical rate baseline is unavailable.
    """
    if not isinstance(telemetry, dict):
        raise TypeError("telemetry must be a dictionary")
    if not isinstance(max_gap_hours, (int, float)) or max_gap_hours <= 0:
        raise ValueError("max_gap_hours must be a positive number")

    configured = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    ratio_threshold = configured["rate_ratio_for_full_score"]
    if not isinstance(ratio_threshold, (int, float)) or ratio_threshold <= 1:
        raise ValueError("rate_ratio_for_full_score must be greater than 1")

    current = _extract_current(telemetry)
    astronaut_id = str(telemetry.get("astronaut_id", "")).strip()
    if not astronaut_id:
        raise ValueError("telemetry must contain astronaut_id")

    current_timestamp = pd.to_datetime(
        current.get("timestamp"), errors="coerce", utc=True
    )
    if pd.isna(current_timestamp):
        raise ValueError("telemetry must contain a valid timestamp")

    current_rate = _valid_rate(
        current.get("radiation_dose_rate_usv_per_hour")
    )

    history_frame = _to_frame(history, "history")
    required = {
        "astronaut_id",
        "timestamp",
        "radiation_dose_rate_usv_per_hour",
    }
    missing = sorted(required - set(history_frame.columns))
    if missing:
        raise ValueError("history is missing required columns: " + ", ".join(missing))

    history_frame["astronaut_id"] = (
        history_frame["astronaut_id"].astype("string").str.strip()
    )
    astronaut_history = history_frame[
        history_frame["astronaut_id"].eq(astronaut_id)
    ].copy()

    history_frame["timestamp"] = pd.to_datetime(
        history_frame["timestamp"], errors="coerce", utc=True
    )
    history_frame["radiation_dose_rate_usv_per_hour"] = pd.to_numeric(
        history_frame["radiation_dose_rate_usv_per_hour"], errors="coerce"
    )

    historical_rates = pd.to_numeric(
        astronaut_history["radiation_dose_rate_usv_per_hour"],
        errors="coerce",
    )
    historical_rates = historical_rates[
        historical_rates.notna() & historical_rates.ge(0)
    ]

    if len(historical_rates):
        historical_mean = float(historical_rates.mean())
        historical_count = int(historical_rates.count())
    else:
        historical_mean = None
        historical_count = 0

    warnings: list[str] = []
    if current_rate is None:
        warnings.append("missing_or_invalid_radiation_dose_rate_usv_per_hour")

    # Integrate historical observations plus the current sample. Keep only
    # this astronaut's rows and do not extrapolate beyond observed timestamps.
    integration_columns = [
        "timestamp",
        "radiation_dose_rate_usv_per_hour",
    ]
    integration_history = astronaut_history.copy()
    integration_history["timestamp"] = pd.to_datetime(
        integration_history["timestamp"], errors="coerce", utc=True
    )
    integration_history["radiation_dose_rate_usv_per_hour"] = pd.to_numeric(
        integration_history["radiation_dose_rate_usv_per_hour"],
        errors="coerce",
    )
    integration_history = integration_history[integration_columns]

    current_row = pd.DataFrame([{
        "timestamp": current_timestamp,
        "radiation_dose_rate_usv_per_hour": current_rate,
    }])
    combined = pd.concat(
        [integration_history, current_row],
        ignore_index=True,
    )

    accumulated_dose, interval_count, skipped_gaps = _integrate_observed_dose(
        combined, float(max_gap_hours)
    )
    if skipped_gaps:
        warnings.append("one_or_more_time_gaps_skipped")

    # Experimental relative-rate indicator. No absolute dose limit is applied.
    if current_rate is None:
        rate_component = {
            "status": "unavailable",
            "score": None,
            "current_rate_usv_per_hour": None,
            "historical_mean_usv_per_hour": historical_mean,
            "explanation": "Current radiation dose-rate measurement is missing or invalid.",
        }
        score = None
        category = "insufficient_data"
        status = "insufficient_data"
    elif historical_mean is None or historical_mean <= 0:
        rate_component = {
            "status": "unavailable",
            "score": None,
            "current_rate_usv_per_hour": current_rate,
            "historical_mean_usv_per_hour": historical_mean,
            "explanation": "A positive historical dose-rate mean is unavailable for comparison.",
        }
        score = None
        category = "insufficient_data"
        status = "insufficient_data"
        warnings.append("insufficient_historical_radiation_rate_baseline")
    else:
        ratio = current_rate / historical_mean
        component_score = round(
            min(max(ratio / float(ratio_threshold), 0.0), 1.0) * 100.0,
            2,
        )
        rate_component = {
            "status": "available",
            "score": component_score,
            "current_rate_usv_per_hour": current_rate,
            "historical_mean_usv_per_hour": historical_mean,
            "current_to_historical_ratio": round(ratio, 4),
            "explanation": (
                f"Current dose rate is {ratio:.2f} times this astronaut's "
                "historical mean dose rate."
            ),
        }
        score = component_score
        if score < 25:
            category = "low"
        elif score < 50:
            category = "moderate"
        elif score < 75:
            category = "elevated"
        else:
            category = "high"
        status = "available"

    return {
        "indicator_name": "radiation",
        "score": score,
        "category": category,
        "status": status,
        "current_dose_rate_usv_per_hour": current_rate,
        "historical_mean_dose_rate_usv_per_hour": historical_mean,
        "historical_valid_readings": historical_count,
        "accumulated_dose_usv": accumulated_dose,
        "integrated_intervals": interval_count,
        "skipped_time_gaps": skipped_gaps,
        "integration_max_gap_hours": float(max_gap_hours),
        "rate_component": rate_component,
        "warnings": warnings,
        "explanation": (
            "Accumulated dose is estimated only across valid observed intervals "
            "using trapezoidal integration. The indicator compares current dose "
            "rate with personal history; no absolute NASA or medical exposure "
            "threshold is applied."
        ),
        "model_version": "radiation-prototype-0.1.0",
        "limitations": [
            "Dose rate is in µSv/hour; accumulated dose is in µSv.",
            "Accumulated dose covers only valid observed intervals in the supplied history plus current record, not lifetime or mission-total exposure.",
            "Intervals longer than max_gap_hours are skipped because exposure during the gap is unknown.",
            "Trapezoidal integration assumes dose rate changes linearly between adjacent observations.",
            "The relative-rate score and category bands are configurable demo assumptions, not NASA safety limits or clinical thresholds.",
            "Synthetic telemetry is for software testing only.",
        ],
    }
