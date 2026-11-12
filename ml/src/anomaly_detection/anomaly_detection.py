"""Experimental Isolation Forest anomaly detection for astronaut telemetry."""
from __future__ import annotations

from typing import Any, Mapping, Sequence

import pandas as pd
from sklearn.ensemble import IsolationForest

IDENTIFIER_COLUMNS = {"astronaut_id", "timestamp", "time", "id"}


def _to_frame(data: Any, name: str) -> pd.DataFrame:
    if isinstance(data, pd.DataFrame):
        return data.copy()
    if isinstance(data, Mapping):
        return pd.DataFrame([dict(data)])
    if isinstance(data, Sequence) and not isinstance(data, (str, bytes)):
        if not all(isinstance(item, Mapping) for item in data):
            raise TypeError(f"{name} sequence must contain record dictionaries")
        return pd.DataFrame([dict(item) for item in data])
    raise TypeError(f"{name} must be a DataFrame, record dictionary, or list of dictionaries")


def _unavailable(message: str, features=None, count: int = 0) -> dict:
    return {
        "status": "insufficient_data",
        "is_anomaly": None,
        "anomaly_score": None,
        "score_interpretation": "Not available.",
        "features_used": features or [],
        "historical_sample_count": int(count),
        "astronaut_id": None,
        "warnings": [message],
    }


def detect_anomalies(
    history: Any,
    current_data: Any,
    *,
    min_history: int = 24,
    contamination: float | str = "auto",
    random_state: int = 42,
    n_estimators: int = 100,
) -> dict:
    """Compare one current record with the same astronaut's historical telemetry.

    Higher anomaly_score values indicate greater statistical deviation. This is
    not a clinical risk score or diagnosis. Missing readings are never imputed
    as zero.
    """
    if not isinstance(min_history, int) or isinstance(min_history, bool) or min_history < 2:
        raise ValueError("min_history must be an integer greater than or equal to 2")
    if not isinstance(n_estimators, int) or isinstance(n_estimators, bool) or n_estimators < 1:
        raise ValueError("n_estimators must be a positive integer")
    if contamination != "auto":
        try:
            value = float(contamination)
        except (TypeError, ValueError) as exc:
            raise ValueError("contamination must be 'auto' or a float in (0, 0.5]") from exc
        if not 0 < value <= 0.5:
            raise ValueError("contamination must be 'auto' or a float in (0, 0.5]")

    hist = _to_frame(history, "history")
    current = _to_frame(current_data, "current_data")
    if len(current) != 1:
        raise ValueError("current_data must contain exactly one current telemetry record")
    if hist.empty:
        return _unavailable("No historical telemetry was provided.")

    astronaut_id = current.iloc[0].get("astronaut_id")
    if astronaut_id is not None and "astronaut_id" in hist.columns:
        hist = hist[hist["astronaut_id"].astype(str).str.strip() == str(astronaut_id).strip()]
    if hist.empty:
        return _unavailable("No historical telemetry exists for this astronaut.")

    candidates = [
        col for col in hist.columns
        if col in current.columns and col not in IDENTIFIER_COLUMNS
    ]
    features = []
    for col in candidates:
        h = pd.to_numeric(hist[col], errors="coerce")
        c = pd.to_numeric(current[col], errors="coerce")
        if h.notna().any() and c.notna().any():
            features.append(col)
    if not features:
        return _unavailable("No shared numeric telemetry features are available.")

    historical = hist[features].apply(pd.to_numeric, errors="coerce")
    present_features = [
        col for col in features
        if pd.notna(pd.to_numeric(current.iloc[0][col], errors="coerce"))
    ]
    if not present_features:
        return _unavailable(
            "The current record has no valid values for shared numeric features.",
            features=features,
        )

    training = historical[present_features].dropna()
    if len(training) < min_history:
        return _unavailable(
            f"Only {len(training)} complete historical rows are available; "
            f"{min_history} are required.",
            features=present_features,
            count=len(training),
        )
    if training.nunique(dropna=True).le(1).all():
        return _unavailable(
            "Historical telemetry has no variation across selected features.",
            features=present_features,
            count=len(training),
        )

    model = IsolationForest(
        n_estimators=n_estimators,
        contamination=contamination,
        random_state=random_state,
    )
    model.fit(training.to_numpy(dtype=float))
    vector = current[present_features].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    decision = float(model.decision_function(vector)[0])
    prediction = int(model.predict(vector)[0])

    return {
        "status": "available",
        "is_anomaly": prediction == -1,
        "anomaly_score": float(-decision),
        "score_interpretation": (
            "Higher values indicate greater statistical deviation; not a clinical risk score."
        ),
        "features_used": present_features,
        "historical_sample_count": int(len(training)),
        "astronaut_id": astronaut_id,
        "warnings": [],
    }
