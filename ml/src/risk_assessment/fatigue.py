"""
Prototype fatigue indicator for COSMOCare.

This is an explainable software-demonstration heuristic, not a clinical
assessment, diagnosis, or validated astronaut-health model.
"""

from __future__ import annotations

from typing import Any


DEFAULT_THRESHOLDS = {
    # A sleep shortfall of this many hours relative to personal baseline
    # maps to 100 component points. This is a configurable demo assumption.
    "sleep_deficit_hours_for_full_score": 2.0,
}

DEFAULT_WEIGHTS = {
    "sleep_hours_last_24h": 0.60,
    "fatigue_level_0_10": 0.40,
}


def _extract_measurements(telemetry: dict[str, Any]) -> dict[str, Any]:
    """Support flat telemetry rows and the shared nested `metrics` shape."""
    nested = telemetry.get("metrics")
    if isinstance(nested, dict):
        return {**telemetry, **nested}
    return telemetry


def _select_baseline(
    baseline: dict[str, Any],
    astronaut_id: str | None,
) -> dict[str, Any]:
    """Accept one astronaut baseline or the full Phase 3 baseline mapping."""
    if not isinstance(baseline, dict):
        return {}
    if "metrics" in baseline:
        return baseline
    if astronaut_id and isinstance(baseline.get(astronaut_id), dict):
        return baseline[astronaut_id]
    return {}


def _available_baseline_mean(metrics: dict[str, Any], metric: str) -> float | None:
    entry = metrics.get(metric)
    if not isinstance(entry, dict) or entry.get("status") != "available":
        return None
    try:
        value = float(entry.get("mean"))
    except (TypeError, ValueError):
        return None
    return value if value >= 0 else None


def _number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number != number or abs(number) == float("inf"):
        return None
    return number


def _score_from_ratio(value: float, full_score_value: float) -> float:
    return round(min(max(value / full_score_value, 0.0), 1.0) * 100.0, 2)


def calculate_fatigue_risk(
    telemetry: dict[str, Any],
    baseline: dict[str, Any],
    thresholds: dict[str, float] | None = None,
) -> dict[str, Any]:
    """
    Calculate an experimental fatigue indicator from sleep and fatigue data.

    Sleep component:
      max(personal_baseline_sleep - current_sleep, 0) /
      sleep_deficit_hours_for_full_score * 100, capped at 100.

    Self-reported fatigue component:
      fatigue_level_0_10 * 10, where 0–10 is the supplied telemetry scale.

    Default weights are sleep 60%, fatigue 40%. Available components are
    renormalized when another component is missing or lacks a sufficient
    individual baseline. Activity level is returned as contextual information
    only; it is not scored because high or low activity alone does not
    consistently indicate fatigue.

    Thresholds and category bands are demo assumptions, not medical limits.
    """
    if not isinstance(telemetry, dict):
        raise TypeError("telemetry must be a dictionary")

    configured_thresholds = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    for key, value in configured_thresholds.items():
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"{key} must be a positive number")

    values = _extract_measurements(telemetry)
    astronaut_id = telemetry.get("astronaut_id")
    selected_baseline = _select_baseline(baseline, astronaut_id)
    baseline_metrics = selected_baseline.get("metrics", {})

    components: dict[str, dict[str, Any]] = {}
    warnings: list[str] = []
    weighted_total = 0.0
    available_weight = 0.0

    # Sleep: compare against an available personal baseline.
    current_sleep = _number(values.get("sleep_hours_last_24h"))
    baseline_sleep = _available_baseline_mean(
        baseline_metrics, "sleep_hours_last_24h"
    )

    if current_sleep is None or not 0 <= current_sleep <= 24:
        components["sleep_hours_last_24h"] = {
            "status": "unavailable",
            "score": None,
            "current_value": None if current_sleep is None else current_sleep,
            "baseline_mean": baseline_sleep,
            "explanation": "Current sleep measurement is missing, invalid, or outside 0–24 hours.",
        }
        warnings.append("missing_or_invalid_sleep_hours_last_24h")
    elif baseline_sleep is None:
        components["sleep_hours_last_24h"] = {
            "status": "unavailable",
            "score": None,
            "current_value": current_sleep,
            "baseline_mean": None,
            "explanation": "A sufficient individual sleep baseline is unavailable.",
        }
        warnings.append("insufficient_baseline_sleep_hours_last_24h")
    else:
        deficit = max(baseline_sleep - current_sleep, 0.0)
        sleep_score = _score_from_ratio(
            deficit,
            float(configured_thresholds["sleep_deficit_hours_for_full_score"]),
        )
        weight = DEFAULT_WEIGHTS["sleep_hours_last_24h"]
        components["sleep_hours_last_24h"] = {
            "status": "available",
            "score": sleep_score,
            "weight": weight,
            "current_value": current_sleep,
            "baseline_mean": baseline_sleep,
            "sleep_deficit_hours": round(deficit, 2),
            "explanation": (
                f"Sleep duration is {deficit:.2f} hours below the individual's "
                "historical mean."
                if deficit > 0
                else "Sleep duration is at or above the individual's historical mean."
            ),
        }
        weighted_total += sleep_score * weight
        available_weight += weight

    # Fatigue: use the supplied 0–10 self-report directly, if present.
    fatigue_value = _number(values.get("fatigue_level_0_10"))
    if fatigue_value is None or not 0 <= fatigue_value <= 10:
        components["fatigue_level_0_10"] = {
            "status": "unavailable",
            "score": None,
            "current_value": fatigue_value,
            "baseline_mean": _available_baseline_mean(
                baseline_metrics, "fatigue_level_0_10"
            ),
            "explanation": "Self-reported fatigue is missing or outside the 0–10 input scale.",
        }
        warnings.append("missing_or_invalid_fatigue_level_0_10")
    else:
        fatigue_score = round(fatigue_value * 10.0, 2)
        weight = DEFAULT_WEIGHTS["fatigue_level_0_10"]
        fatigue_baseline = _available_baseline_mean(
            baseline_metrics, "fatigue_level_0_10"
        )
        components["fatigue_level_0_10"] = {
            "status": "available",
            "score": fatigue_score,
            "weight": weight,
            "current_value": fatigue_value,
            "baseline_mean": fatigue_baseline,
            "explanation": (
                f"Current self-reported fatigue is {fatigue_value:.1f} on the 0–10 scale."
            ),
        }
        weighted_total += fatigue_score * weight
        available_weight += weight

    # Activity is context only; it is deliberately excluded from the score.
    activity_value = _number(values.get("activity_level_percent"))
    activity_baseline = _available_baseline_mean(
        baseline_metrics, "activity_level_percent"
    )
    if activity_value is not None and 0 <= activity_value <= 100:
        activity_context = {
            "status": "available",
            "current_value": activity_value,
            "baseline_mean": activity_baseline,
            "used_in_score": False,
            "explanation": (
                "Activity is shown as context only and is not scored because "
                "activity level alone does not establish fatigue."
            ),
        }
    else:
        activity_context = {
            "status": "unavailable",
            "current_value": None,
            "baseline_mean": activity_baseline,
            "used_in_score": False,
            "explanation": "Activity measurement is missing or invalid; it is not required for this prototype score.",
        }

    if available_weight == 0:
        overall_score = None
        category = "insufficient_data"
        status = "insufficient_data"
        summary = "Fatigue indicator unavailable because neither sleep nor self-reported fatigue could be scored."
    else:
        overall_score = round(weighted_total / available_weight, 2)
        if overall_score < 25:
            category = "low"
        elif overall_score < 50:
            category = "moderate"
        elif overall_score < 75:
            category = "elevated"
        else:
            category = "high"
        status = "available"
        summary = (
            "Experimental fatigue indicator based on sleep shortfall from "
            "personal history and/or self-reported fatigue; not a clinical assessment."
        )

    return {
        "indicator_name": "fatigue",
        "score": overall_score,
        "category": category,
        "status": status,
        "components": components,
        "context": {"activity_level_percent": activity_context},
        "warnings": warnings,
        "explanation": summary,
        "model_version": "fatigue-prototype-0.1.0",
        "limitations": [
            "Prototype heuristic; not clinically validated or diagnostic.",
            "Sleep threshold, weights, and category bands are configurable demo assumptions.",
            "Activity is contextual only and is not counted as an independent fatigue signal.",
            "Missing measurements and insufficient sleep baselines are not treated as zero risk.",
            "Self-reported fatigue is assumed to use the supplied 0–10 scale.",
        ],
    }
