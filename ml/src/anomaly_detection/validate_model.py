"""
Independently validate the optimized COSMOCare Isolation Forest.

The model is trained using the original training dataset.
The separate validation dataset is used only for evaluation.
"""

from __future__ import annotations

import json
from pathlib import Path

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

from ml.src.preprocessing.telemetry_preprocessing import (
    preprocess_telemetry,
)


# Project paths
REPO_ROOT = Path(__file__).resolve().parents[3]

TRAIN_DATA_PATH = (
    REPO_ROOT / "ml" / "data" / "raw" / "astronaut_telemetry.csv"
)

VALIDATION_DATA_PATH = (
    REPO_ROOT / "ml" / "data" / "validation" / "astronaut_validation.csv"
)

OUTPUT_PATH = (
    REPO_ROOT / "ml" / "models" / "validation_metrics.json"
)


# Optimized configuration from the previous experiment
MODEL_PARAMETERS = {
    "n_estimators": 200,
    "contamination": 0.03,
    "max_samples": 0.8,
    "max_features": 0.8,
    "random_state": 42,
    "n_jobs": -1,
}

# Threshold selected during out-of-fold threshold optimization
SELECTED_THRESHOLD = -0.5216710512408959


FEATURE_COLUMNS = [
    "heart_rate_bpm",
    "spo2_percent",
    "sleep_hours_last_24h",
    "body_temperature_celsius",
    "radiation_dose_rate_usv_per_hour",
    "activity_level_percent",
    "fatigue_level_0_10",
]


def load_dataset(path: Path) -> pd.DataFrame:
    """Load and preprocess a telemetry dataset."""

    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    raw_data = pd.read_csv(path)
    processed_data = preprocess_telemetry(raw_data)

    required_columns = FEATURE_COLUMNS + ["anomaly_label"]

    missing_columns = [
        column
        for column in required_columns
        if column not in processed_data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return processed_data


def prepare_features(data: pd.DataFrame):
    """Prepare numeric features and synthetic evaluation labels."""

    features = data[FEATURE_COLUMNS].apply(
        pd.to_numeric,
        errors="coerce",
    )

    labels = pd.to_numeric(
        data["anomaly_label"],
        errors="coerce",
    )

    valid_rows = labels.isin([0, 1])

    features = features.loc[valid_rows]
    labels = labels.loc[valid_rows].astype(int)

    if labels.nunique() != 2:
        raise ValueError(
            "Dataset must contain both normal and anomaly records."
        )

    return features, labels.to_numpy()


def train_optimized_model(training_data: pd.DataFrame):
    """Train the optimized Isolation Forest using training data only."""

    X_train, _ = prepare_features(training_data)

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

    # Labels are deliberately excluded from training.
    pipeline.fit(X_train)

    return pipeline


def evaluate_model(model, validation_data: pd.DataFrame):
    """Evaluate the trained model using the selected score threshold."""

    X_validation, y_true = prepare_features(validation_data)

    # Apply the imputer fitted on training data.
    imputer = model.named_steps["imputer"]

    X_validation_imputed = imputer.transform(
        X_validation
    )

    # Obtain anomaly scores from the trained Isolation Forest.
    isolation_forest = model.named_steps["isolation_forest"]

    anomaly_scores = isolation_forest.score_samples(
        X_validation_imputed
    )

    # Lower score_samples values indicate more anomalous records.
    predictions = (
        anomaly_scores <= SELECTED_THRESHOLD
    ).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        predictions,
        labels=[0, 1],
    ).ravel()

    precision = precision_score(
        y_true,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_true,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_true,
        predictions,
        zero_division=0,
    )

    accuracy = accuracy_score(
        y_true,
        predictions,
    )

    false_positive_rate = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0.0
    )

    return {
        "evaluation_method": (
            "Independent synthetic validation dataset"
        ),
        "training_dataset": str(TRAIN_DATA_PATH),
        "validation_dataset": str(VALIDATION_DATA_PATH),
        "training_method": (
            "Unsupervised Isolation Forest; labels excluded from training"
        ),
        "model_parameters": MODEL_PARAMETERS,
        "selected_threshold": SELECTED_THRESHOLD,
        "threshold_source": (
            "Previous 3-fold out-of-fold threshold optimization"
        ),
        "validation_records": int(len(y_true)),
        "normal_records": int(np.sum(y_true == 0)),
        "anomaly_records": int(np.sum(y_true == 1)),
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
            y_true,
            predictions,
            labels=[0, 1],
            target_names=["normal", "anomaly"],
            output_dict=True,
            zero_division=0,
        ),
        "warning": (
            "Results use synthetic telemetry and do not represent "
            "clinical validation or real astronaut performance. "
            "The selected threshold was obtained from cross-validation "
            "on the training dataset; its transfer to the final model "
            "must be interpreted cautiously."
        ),
    }


def main():
    print("Loading training dataset...")

    training_data = load_dataset(TRAIN_DATA_PATH)

    print(
        f"Training records: {len(training_data)}"
    )

    print("\nLoading independent validation dataset...")

    validation_data = load_dataset(VALIDATION_DATA_PATH)

    print(
        f"Validation records: {len(validation_data)}"
    )

    print("\nTraining optimized Isolation Forest...")

    model = train_optimized_model(training_data)

    print("Model training completed.")

    print("\nEvaluating on independent validation data...")

    metrics = evaluate_model(
        model,
        validation_data,
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        json.dumps(metrics, indent=4),
        encoding="utf-8",
    )

    print("\nIndependent validation completed.")

    print("\nValidation results:")

    print(
        json.dumps(
            {
                key: value
                for key, value in metrics.items()
                if key != "classification_report"
            },
            indent=4,
        )
    )

    print(
        f"\nResults saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()