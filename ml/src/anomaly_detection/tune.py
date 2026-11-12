"""
Isolation Forest Hyperparameter Optimization.

Tests different configurations using stratified cross-validation.
Does not modify or overwrite the existing trained model.
"""

import itertools
import json
from pathlib import Path

import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import StratifiedKFold

from ml.src.preprocessing.telemetry_preprocessing import preprocess_telemetry


# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_PATH = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "raw"
    / "astronaut_telemetry.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "optimization_results.json"
)


# --------------------------------------------------
# FEATURE CONFIGURATION
# --------------------------------------------------

FEATURE_COLUMNS = [
    "heart_rate_bpm",
    "spo2_percent",
    "sleep_hours_last_24h",
    "body_temperature_celsius",
    "radiation_dose_rate_usv_per_hour",
    "activity_level_percent",
    "fatigue_level_0_10",
]


# --------------------------------------------------
# MODEL EVALUATION
# --------------------------------------------------

def evaluate_configuration(
    X,
    y,
    n_estimators,
    contamination,
    max_samples,
    max_features,
):
    """Evaluate one configuration using stratified cross-validation."""

    splitter = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=42,
    )

    actual_all = []
    predicted_all = []

    for train_index, test_index in splitter.split(X, y):

        X_train = X.iloc[train_index]
        X_test = X.iloc[test_index]

        y_test = y.iloc[test_index]

        # Fit preprocessing only on training data.
        imputer = SimpleImputer(strategy="median")

        X_train_clean = imputer.fit_transform(X_train)
        X_test_clean = imputer.transform(X_test)

        # Create Isolation Forest.
        model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            max_samples=max_samples,
            max_features=max_features,
            random_state=42,
            n_jobs=-1,
        )

        # Train without using anomaly labels.
        model.fit(X_train_clean)

        predictions = (
            model.predict(X_test_clean) == -1
        ).astype(int)

        actual_all.extend(y_test.tolist())
        predicted_all.extend(predictions.tolist())

    precision = precision_score(
        actual_all,
        predicted_all,
        zero_division=0,
    )

    recall = recall_score(
        actual_all,
        predicted_all,
        zero_division=0,
    )

    f1 = f1_score(
        actual_all,
        predicted_all,
        zero_division=0,
    )

    matrix = confusion_matrix(
        actual_all,
        predicted_all,
        labels=[0, 1],
    )

    tn, fp, fn, tp = matrix.ravel()

    false_positive_rate = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0.0
    )

    return {
        "n_estimators": n_estimators,
        "contamination": contamination,
        "max_samples": max_samples,
        "max_features": max_features,
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "false_positive_rate": float(false_positive_rate),
        "true_positives": int(tp),
        "false_positives": int(fp),
        "true_negatives": int(tn),
        "false_negatives": int(fn),
    }


# --------------------------------------------------
# MAIN OPTIMIZATION FUNCTION
# --------------------------------------------------

def main():

    print("Loading historical telemetry...")

    raw = pd.read_csv(DATA_PATH)

    clean = preprocess_telemetry(raw)

    if "anomaly_label" not in clean.columns:
        raise ValueError(
            "Dataset must contain anomaly_label."
        )

    labels = pd.to_numeric(
        clean["anomaly_label"],
        errors="coerce",
    )

    valid = labels.isin([0, 1])

    X = (
        clean.loc[valid, FEATURE_COLUMNS]
        .apply(pd.to_numeric, errors="coerce")
        .reset_index(drop=True)
    )

    y = (
        labels.loc[valid]
        .astype(int)
        .reset_index(drop=True)
    )

    # Remove features containing only missing values.
    X = X.dropna(axis=1, how="all")

    if y.value_counts().min() < 3:
        raise ValueError(
            "At least three examples of each class "
            "are required for three-fold cross-validation."
        )

    print(f"Dataset records: {len(X)}")
    print(f"Normal records: {(y == 0).sum()}")
    print(f"Anomaly records: {(y == 1).sum()}")

    print(f"Features: {list(X.columns)}")

    # Hyperparameter combinations.
    parameter_grid = {
        "n_estimators": [200, 400],
        "contamination": [
            0.01,
            0.02,
            0.03,
            0.05,
            0.08,
            0.10,
        ],
        "max_samples": ["auto", 0.8],
        "max_features": [0.8, 1.0],
    }

    combinations = list(
        itertools.product(
            parameter_grid["n_estimators"],
            parameter_grid["contamination"],
            parameter_grid["max_samples"],
            parameter_grid["max_features"],
        )
    )

    results = []

    print(
        f"\nTesting {len(combinations)} configurations..."
    )

    for index, combination in enumerate(
        combinations,
        start=1,
    ):

        (
            n_estimators,
            contamination,
            max_samples,
            max_features,
        ) = combination

        result = evaluate_configuration(
            X=X,
            y=y,
            n_estimators=n_estimators,
            contamination=contamination,
            max_samples=max_samples,
            max_features=max_features,
        )

        results.append(result)

        print(
            f"[{index}/{len(combinations)}] "
            f"Contamination={contamination}, "
            f"Trees={n_estimators}, "
            f"F1={result['f1_score']:.4f}, "
            f"Precision={result['precision']:.4f}, "
            f"Recall={result['recall']:.4f}, "
            f"FPR={result['false_positive_rate']:.4f}"
        )

    # Rank configurations by F1, precision and recall.
    results.sort(
        key=lambda item: (
            item["f1_score"],
            item["precision"],
            item["recall"],
        ),
        reverse=True,
    )

    output = {
        "evaluation_method": (
            "Three-fold stratified cross-validation. "
            "Synthetic labels used only for evaluation."
        ),
        "dataset_records": int(len(X)),
        "normal_records": int((y == 0).sum()),
        "anomaly_records": int((y == 1).sum()),
        "features": list(X.columns),
        "configurations_tested": len(results),
        "best_configuration": results[0],
        "all_results": results,
        "warning": (
            "Synthetic evaluation only. "
            "Not clinical validation or real astronaut performance."
        ),
    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        json.dumps(output, indent=4),
        encoding="utf-8",
    )

    print("\n========== BEST CONFIGURATION ==========")

    print(
        json.dumps(
            results[0],
            indent=4,
        )
    )

    print(
        f"\nResults saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()