"""
Train, evaluate, and persist the COSMOCare Isolation Forest.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline


REPO_ROOT = Path(__file__).resolve().parents[3]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml.src.preprocessing.telemetry_preprocessing import (
    preprocess_telemetry,
)


FEATURE_COLUMNS = [
    "heart_rate_bpm",
    "spo2_percent",
    "sleep_hours_last_24h",
    "body_temperature_celsius",
    "radiation_dose_rate_usv_per_hour",
    "activity_level_percent",
    "fatigue_level_0_10",
]

MODEL_VERSION = "1.1.0"

MODEL_PARAMETERS = {
    "n_estimators": 200,
    "contamination": 0.03,
    "max_samples": 0.8,
    "max_features": 0.8,
    "random_state": 42,
    "n_jobs": -1,
}

SELECTED_THRESHOLD = -0.5216710512408959


def load_dataset(data_path: str | Path):
    """Load and preprocess telemetry data."""

    path = Path(data_path)

    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found: {path}")

    raw = pd.read_csv(path)
    clean = preprocess_telemetry(raw)

    required_columns = FEATURE_COLUMNS + ["anomaly_label"]

    missing = [
        column
        for column in required_columns
        if column not in clean.columns
    ]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    labels = pd.to_numeric(
        clean["anomaly_label"],
        errors="coerce",
    )

    valid = labels.isin([0, 1])

    features = clean.loc[valid, FEATURE_COLUMNS].apply(
        pd.to_numeric,
        errors="coerce",
    )

    labels = labels.loc[valid].astype(int)

    if labels.nunique() != 2:
        raise ValueError(
            "Dataset must contain normal and anomaly records."
        )

    return features, labels.to_numpy()


def train_model(
    data_path: str | Path,
    model_path: str | Path,
    metrics_path: str | Path,
    validation_path: str | Path,
) -> dict:
    """Train on training data and evaluate on separate validation data."""

    print("Loading training dataset...")

    X_train, _ = load_dataset(data_path)

    print(f"Training records: {len(X_train)}")

    print("\nLoading independent validation dataset...")

    X_validation, y_validation = load_dataset(validation_path)

    print(f"Validation records: {len(X_validation)}")

    pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),
        (
            "isolation_forest",
            IsolationForest(**MODEL_PARAMETERS),
        ),
    ])

    print("\nTraining optimized Isolation Forest...")

    # Unsupervised training: anomaly labels are not used.
    pipeline.fit(X_train)

    print("Training completed.")

    # Apply the imputer learned from training data.
    validation_imputed = pipeline.named_steps["imputer"].transform(
        X_validation
    )

    isolation_forest = pipeline.named_steps["isolation_forest"]

    # Lower score_samples values indicate more anomalous records.
    anomaly_scores = isolation_forest.score_samples(
        validation_imputed
    )

    predictions = (
        anomaly_scores <= SELECTED_THRESHOLD
    ).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_validation,
        predictions,
        labels=[0, 1],
    ).ravel()

    precision = precision_score(
        y_validation,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_validation,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_validation,
        predictions,
        zero_division=0,
    )

    accuracy = accuracy_score(
        y_validation,
        predictions,
    )

    false_positive_rate = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0.0
    )

    metrics = {
        "model_version": MODEL_VERSION,
        "evaluation_method": "Independent synthetic validation dataset",
        "training_method": "Unsupervised Isolation Forest",
        "training_labels_used": False,
        "training_rows": int(len(X_train)),
        "validation_rows": int(len(X_validation)),
        "features": FEATURE_COLUMNS,
        "model_parameters": MODEL_PARAMETERS,
        "selected_threshold": SELECTED_THRESHOLD,
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "accuracy": float(accuracy),
        "false_positive_rate": float(false_positive_rate),
        "confusion_matrix_labels_0_normal_1_anomaly": [
            [int(tn), int(fp)],
            [int(fn), int(tp)],
        ],
        "classification_report": classification_report(
            y_validation,
            predictions,
            labels=[0, 1],
            target_names=["normal", "anomaly"],
            output_dict=True,
            zero_division=0,
        ),
        "warning": (
            "Metrics use synthetic telemetry and do not represent "
            "clinical validation or real astronaut performance."
        ),
    }

    artifact = {
        "model": pipeline,
        "feature_columns": FEATURE_COLUMNS,
        "threshold": SELECTED_THRESHOLD,
        "metadata": {
            "model_version": MODEL_VERSION,
            "model_type": "IsolationForest",
            "training_rows": int(len(X_train)),
            "model_parameters": MODEL_PARAMETERS,
            "threshold": SELECTED_THRESHOLD,
            "threshold_source": (
                "Three-fold out-of-fold threshold optimization"
            ),
            "features": FEATURE_COLUMNS,
        },
    }

    model_file = Path(model_path)
    model_file.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(artifact, model_file)

    metrics_file = Path(metrics_path)
    metrics_file.parent.mkdir(parents=True, exist_ok=True)

    metrics_file.write_text(
        json.dumps(metrics, indent=4),
        encoding="utf-8",
    )

    print("\nTraining and evaluation completed.")
    print(json.dumps(metrics, indent=4))
    print(f"\nSaved trained model: {model_file}")
    print(f"Saved evaluation metrics: {metrics_file}")

    return metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--data",
        default=str(
            REPO_ROOT / "ml/data/raw/astronaut_telemetry.csv"
        ),
    )

    parser.add_argument(
        "--validation",
        default=str(
            REPO_ROOT / "ml/data/validation/astronaut_validation.csv"
        ),
    )

    parser.add_argument(
        "--model",
        default=str(
            REPO_ROOT / "ml/models/isolation_forest.joblib"
        ),
    )

    parser.add_argument(
        "--metrics",
        default=str(
            REPO_ROOT / "ml/models/evaluation_metrics.json"
        ),
    )

    args = parser.parse_args()

    train_model(
        args.data,
        args.model,
        args.metrics,
        args.validation,
    )


if __name__ == "__main__":
    main()