"""
Load and reuse the persisted COSMOCare Isolation Forest artifact.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import joblib
import numpy as np
import pandas as pd


DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "models"
    / "isolation_forest.joblib"
)


def load_anomaly_model(
    model_path: str | Path = DEFAULT_MODEL_PATH,
) -> dict:
    """Load a trained model artifact for reuse by the backend."""

    path = Path(model_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Trained anomaly model not found: {path}. "
            "Run train.py first."
        )

    artifact = joblib.load(path)

    required = {
        "model",
        "feature_columns",
        "metadata",
    }

    if not isinstance(artifact, dict) or not required.issubset(artifact):
        raise ValueError("Invalid anomaly model artifact format.")

    if "threshold" not in artifact:
        raise ValueError(
            "Model artifact does not contain a decision threshold. "
            "Retrain the model using the updated train.py."
        )

    if not np.isfinite(artifact["threshold"]):
        raise ValueError("Model threshold must be a finite number.")

    return artifact


def predict_anomaly(
    data: Mapping[str, Any] | pd.DataFrame,
    artifact: dict,
) -> dict:
    """
    Predict anomalies using the persisted model.

    This function performs inference only.
    It never trains or refits the model.
    """

    frame = (
        data.copy()
        if isinstance(data, pd.DataFrame)
        else pd.DataFrame([dict(data)])
    )

    if len(frame) != 1:
        raise ValueError(
            "data must contain exactly one telemetry record."
        )

    features = artifact["feature_columns"]

    row = frame.reindex(columns=features)

    if row.iloc[0].isna().all():
        return {
            "status": "insufficient_data",
            "is_anomaly": None,
            "anomaly_score": None,
            "features_used": features,
            "warnings": [
                "No valid model features in current telemetry."
            ],
        }

    model = artifact["model"]

    # The persisted pipeline handles missing-value imputation.
    imputer = model.named_steps["imputer"]

    isolation_forest = model.named_steps["isolation_forest"]

    transformed = imputer.transform(row)

    # Use the same score_samples convention as training.
    score = float(
        isolation_forest.score_samples(transformed)[0]
    )

    threshold = float(artifact["threshold"])

    is_anomaly = score <= threshold

    return {
        "status": "available",
        "is_anomaly": bool(is_anomaly),
        "anomaly_score": float(-score),
        "decision_threshold": threshold,
        "model_version": artifact["metadata"].get(
            "model_version"
        ),
        "features_used": features,
        "warnings": [
            "Statistical anomaly flag; not a clinical diagnosis."
        ],
    }