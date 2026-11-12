"""
Overall astronaut risk engine for COSMOCare.

Combines the prototype cardiovascular, fatigue, and radiation indicators.
This is an experimental decision-support prototype, not a diagnosis or a
clinically validated astronaut-health risk model.
"""

from __future__ import annotations

from typing import Any

from .cardiovascular import calculate_cardiovascular_risk
from .fatigue import calculate_fatigue_risk
from .radiation import calculate_radiation_risk


DEFAULT_WEIGHTS = {
    "cardiovascular": 0.40,
    "fatigue": 0.35,
    "radiation": 0.25,
}


def _unavailable_indicator(name: str, reason: str) -> dict[str, Any]:
    return {
        "indicator_name": name,
        "score": None,
        "category": "insufficient_data",
        "status": "insufficient_data",
        "warnings": [reason],
        "explanation": reason,
    }


def _validate_weights(weights: dict[str, float] | None) -> dict[str, float]:
    configured = {**DEFAULT_WEIGHTS, **(weights or {})}

    for name in DEFAULT_WEIGHTS:
        value = configured[name]
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Weight for {name} must be a non-negative number")

    if sum(configured.values()) <= 0:
        raise ValueError("At least one risk-indicator weight must be positive")

    return {name: float(configured[name]) for name in DEFAULT_WEIGHTS}


def calculate_risk(
    telemetry: dict[str, Any],
    baseline: dict[str, Any],
    history: Any = None,
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """
    Calculate overall experimental risk from the three indicator modules.

    Parameters
    ----------
    telemetry:
        Current astronaut telemetry record. Supports flat measurement keys
        and the shared nested `metrics` structure.
    baseline:
        Baseline mapping or one astronaut's baseline object returned by
        Phase 3 `calculate_baseline`.
    history:
        Historical telemetry records required by the radiation module for
        dose-rate comparison and observed-interval dose integration. Pass
        records for the same astronaut, preferably excluding the current
        record. If omitted, radiation is marked unavailable.
    weights:
        Optional indicator weights. Defaults are cardiovascular 40%,
        fatigue 35%, radiation 25%.

    Missing-data policy
    -------------------
    An indicator contributes only if its result has a numeric score and
    status `available`. The final weighted average is renormalized over
    available indicators. Unavailable indicators are listed in the output
    and are never silently converted to zero risk.

    Returns
    -------
    dict:
        Overall score/category/status, the three detailed indicator results,
        configured and effective weights, warnings, and explanation.
    """
    if not isinstance(telemetry, dict):
        raise TypeError("telemetry must be a dictionary")

    configured_weights = _validate_weights(weights)

    indicators: dict[str, dict[str, Any]] = {}

    # Each indicator is independently computed. A missing/invalid input for
    # one category must not prevent other usable categories from contributing.
    try:
        indicators["cardiovascular"] = calculate_cardiovascular_risk(
            telemetry, baseline
        )
    except (TypeError, ValueError, KeyError) as exc:
        indicators["cardiovascular"] = _unavailable_indicator(
            "cardiovascular",
            f"Cardiovascular indicator could not be calculated: {exc}",
        )

    try:
        indicators["fatigue"] = calculate_fatigue_risk(
            telemetry, baseline
        )
    except (TypeError, ValueError, KeyError) as exc:
        indicators["fatigue"] = _unavailable_indicator(
            "fatigue",
            f"Fatigue indicator could not be calculated: {exc}",
        )

    if history is None:
        indicators["radiation"] = _unavailable_indicator(
            "radiation",
            "Historical telemetry was not supplied; radiation indicator is unavailable.",
        )
    else:
        try:
            indicators["radiation"] = calculate_radiation_risk(
                telemetry, history
            )
        except (TypeError, ValueError, KeyError) as exc:
            indicators["radiation"] = _unavailable_indicator(
                "radiation",
                f"Radiation indicator could not be calculated: {exc}",
            )

    available = {
        name: result
        for name, result in indicators.items()
        if result.get("status") == "available"
        and isinstance(result.get("score"), (int, float))
    }

    available_weight_total = sum(configured_weights[name] for name in available)
    effective_weights: dict[str, float] = {}
    warnings: list[str] = []

    for name, result in indicators.items():
        if name not in available:
            effective_weights[name] = 0.0
            warnings.append(f"{name}_indicator_unavailable")
        elif available_weight_total > 0:
            effective_weights[name] = round(
                configured_weights[name] / available_weight_total, 6
            )
        else:
            effective_weights[name] = 0.0

        for warning in result.get("warnings", []):
            warnings.append(f"{name}:{warning}")

    if not available or available_weight_total <= 0:
        overall_score = None
        category = "insufficient_data"
        status = "insufficient_data"
        explanation = (
            "Overall risk is unavailable because no indicator with a "
            "positive configured weight could be calculated."
        )
    else:
        overall_score = round(
            sum(
                float(available[name]["score"]) * effective_weights[name]
                for name in available
            ),
            2,
        )

        if overall_score < 25:
            category = "low"
        elif overall_score < 50:
            category = "moderate"
        elif overall_score < 75:
            category = "elevated"
        else:
            category = "high"

        status = (
            "available"
            if len(available) == len(indicators)
            else "partially_available"
        )
        included = ", ".join(sorted(available.keys()))
        excluded = sorted(set(indicators) - set(available))
        explanation = (
            f"Overall experimental score combines available indicators: {included}. "
            "Weights were renormalized over available indicators only."
        )
        if excluded:
            explanation += (
                " Unavailable indicators were excluded, not treated as zero risk: "
                + ", ".join(excluded)
                + "."
            )

    return {
        "indicator_name": "overall_risk",
        "score": overall_score,
        "category": category,
        "status": status,
        "indicators": indicators,
        "configured_weights": configured_weights,
        "effective_weights": effective_weights,
        "available_indicator_count": len(available),
        "total_indicator_count": len(indicators),
        "warnings": warnings,
        "explanation": explanation,
        "model_version": "overall-risk-prototype-0.1.0",
        "limitations": [
            "Experimental prototype; not clinically validated, diagnostic, or a medical recommendation.",
            "Default indicator weights (cardiovascular 40%, fatigue 35%, radiation 25%) are project assumptions, not scientifically validated coefficients.",
            "Indicator category bands are software-demo bands, not medical or NASA safety thresholds.",
            "Unavailable indicators are excluded and available weights are renormalized; this can change score interpretation when data is missing.",
            "Radiation assessment requires historical telemetry and estimates only observed intervals.",
            "Synthetic telemetry is for software testing and demonstration, not real astronaut physiology.",
        ],
    }
