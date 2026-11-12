"""
Prototype cardiovascular indicator for COSMOCare.

This is an explainable software demonstration heuristic, not a clinical
assessment, diagnosis, or validated astronaut-health model.
"""

from __future__ import annotations

from typing import Any


DEFAULT_THRESHOLDS = {
    # Full component score at or beyond these deviations from personal baseline.
    "heart_rate_relative_deviation": 0.20,  # 20% from baseline mean
    "spo2_drop_percentage_points": 4.0,     # 4 percentage points below baseline mean
}

DEFAULT_WEIGHTS = {
    "heart_rate_bpm": 0.60,
    "spo2_percent": 0.40,
}


def _extract_measurements(telemetry: dict[str, Any]) -> dict[str, Any]:
    """Support flat telemetry rows and the shared nested `metrics` shape."""
    nested = telemetry.get("metrics")
    if isinstance(nested, dict):
        return {**telemetry, **nested}
    return telemetry


def _extract_baseline(baseline: dict[str, Any], astronaut_id: str | None) -> dict[str, Any]:
    """
    Accept either one astronaut's baseline object or the full mapping returned
    by calculate_baseline().
    """
    if not isinstance(baseline, dict):
        return {}

    if "metrics" in baseline:
        return baseline

    if astronaut_id and astronaut_id in baseline:
        candidate = baseline[astronaut_id]
        if isinstance(candidate, dict):
            return candidate

    return {}


def _metric_baseline(baseline_metrics: dict[str, Any], metric: str) -> float | None:
    entry = baseline_metrics.get(metric)
    if not isinstance(entry, dict):
        return None
    if entry.get("status") != "available":
        return None

    value = entry.get("mean")
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None

    return numeric if numeric > 0 else None


def _bounded_score(deviation: float, full_score_deviation: float) -> float:
    """Map a non-negative deviation to a transparent 0–100 component score."""
    if full_score_deviation <= 0:
        raise ValueError("score threshold must be greater than zero")
    return round(min(max(deviation / full_score_deviation, 0.0), 1.0) * 100.0, 2)


def calculate_cardiovascular_risk(
    telemetry: dict[str, Any],
    baseline: dict[str, Any],
    thresholds: dict[str, float] | None = None,
) -> dict[str, Any]:
    """
    Calculate an experimental cardiovascular indicator from HR and SpO2.

    Required input fields:
      telemetry: astronaut_id plus heart_rate_bpm and/or spo2_percent.
      baseline: one astronaut baseline object, or the complete mapping
                returned by calculate_baseline().

    A metric contributes only when its current value is valid and its
    historical baseline status is `available`. Missing/insufficient metrics
    are excluded from the weighted average and listed as warnings; they are
    never treated as zero risk.

    Prototype component formula:
      HR score = min(abs(current_hr - baseline_hr) /
                     (baseline_hr * 0.20), 1) * 100
      SpO2 score = min(max(baseline_spo2 - current_spo2, 0) / 4, 1) * 100
      Overall score = weighted mean of available component scores
                      (HR 60%, SpO2 40%, renormalized if one is unavailable).

    The thresholds and weights are configurable prototype assumptions, not
    medical thresholds. The returned category is a software-demo band only.
    """
    if not isinstance(telemetry, dict):
        raise TypeError("telemetry must be a dictionary")

    configured_thresholds = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    for key, value in configured_thresholds.items():
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"{key} must be a positive number")

    values = _extract_measurements(telemetry)
    astronaut_id = telemetry.get("astronaut_id")
    selected_baseline = _extract_baseline(baseline, astronaut_id)
    baseline_metrics = selected_baseline.get("metrics", {})

    components: dict[str, dict[str, Any]] = {}
    warnings: list[str] = []
    weighted_total = 0.0
    available_weight = 0.0

    current_specs = (
        ("heart_rate_bpm", "heart_rate_relative_deviation"),
        ("spo2_percent", "spo2_drop_percentage_points"),
    )

    for metric, threshold_key in current_specs:
        current_raw = values.get(metric)
        base_mean = _metric_baseline(baseline_metrics, metric)

        try:
            current = float(current_raw)
            if not (current == current and abs(current) != float("inf")):
                raise ValueError
        except (TypeError, ValueError):
            current = None

        if current is None:
            components[metric] = {
                "status": "unavailable",
                "score": None,
                "current_value": None,
                "baseline_mean": base_mean,
                "explanation": "Current measurement is missing or invalid.",
            }
            warnings.append(f"missing_or_invalid_{metric}")
            continue

        if base_mean is None:
            components[metric] = {
                "status": "unavailable",
                "score": None,
                "current_value": current,
                "baseline_mean": None,
                "explanation": "A sufficient individual historical baseline is unavailable.",
            }
            warnings.append(f"insufficient_baseline_{metric}")
            continue

        if metric == "heart_rate_bpm":
            if current <= 0:
                components[metric] = {
                    "status": "unavailable",
                    "score": None,
                    "current_value": current,
                    "baseline_mean": base_mean,
                    "explanation": "Current measurement is outside the accepted data-quality range.",
                }
                warnings.append(f"invalid_{metric}")
                continue
            deviation = abs(current - base_mean) / base_mean
            score = _bounded_score(
                deviation,
                float(configured_thresholds[threshold_key]),
            )
            explanation = (
                f"Heart rate differs from the individual's historical mean "
                f"by {deviation * 100:.1f}%."
            )
        else:
            if not 0 <= current <= 100:
                components[metric] = {
                    "status": "unavailable",
                    "score": None,
                    "current_value": current,
                    "baseline_mean": base_mean,
                    "explanation": "Current measurement is outside the accepted data-quality range.",
                }
                warnings.append(f"invalid_{metric}")
                continue
            drop = max(base_mean - current, 0.0)
            score = _bounded_score(
                drop,
                float(configured_thresholds[threshold_key]),
            )
            explanation = (
                f"SpO2 is {drop:.1f} percentage points below the individual's "
                f"historical mean."
            )

        weight = DEFAULT_WEIGHTS[metric]
        components[metric] = {
            "status": "available",
            "score": score,
            "weight": weight,
            "current_value": current,
            "baseline_mean": base_mean,
            "explanation": explanation,
        }
        weighted_total += score * weight
        available_weight += weight

    if available_weight == 0:
        overall_score = None
        category = "insufficient_data"
        summary = "Cardiovascular indicator unavailable because no usable current measurements and individual baselines were available."
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
        summary = (
            "Experimental indicator based on deviations from the individual's "
            "historical heart-rate and SpO2 means; not a clinical assessment."
        )

    return {
        "indicator_name": "cardiovascular",
        "score": overall_score,
        "category": category,
        "status": "available" if overall_score is not None else "insufficient_data",
        "components": components,
        "warnings": warnings,
        "explanation": summary,
        "model_version": "cardiovascular-prototype-0.1.0",
        "limitations": [
            "Prototype heuristic; not clinically validated or diagnostic.",
            "Score bands and deviation thresholds are configurable demo assumptions, not medical thresholds.",
            "Requires sufficient astronaut-specific historical baselines.",
            "Missing measurements and insufficient baselines are not treated as zero risk.",
        ],
    }
