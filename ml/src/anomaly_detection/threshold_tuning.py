import json
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
)
from sklearn.model_selection import StratifiedKFold

from preprocessing.telemetry_preprocessing import preprocess_telemetry


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "astronaut_telemetry.csv"

OUTPUT_PATH = (
    PROJECT_ROOT / "models" / "threshold_optimization_results.json"
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

RANDOM_STATE = 42

# Candidate Isolation Forest score thresholds.
# Lower scores indicate more anomalous observations.
THRESHOLD_QUANTILES = np.arange(0.01, 0.201, 0.01)


def load_dataset():
    """Load and preprocess the telemetry dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Telemetry dataset not found: {DATA_PATH}"
        )

    data = pd.read_csv(DATA_PATH)

    processed_data = preprocess_telemetry(data)

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


def evaluate_threshold(y_true, anomaly_scores, threshold):
    """Evaluate predictions using a selected score threshold."""

    # Isolation Forest assigns lower scores to more anomalous records.
    predictions = (anomaly_scores <= threshold).astype(int)

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

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        predictions,
        labels=[0, 1],
    ).ravel()

    false_positive_rate = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0.0
    )

    return {
        "threshold": float(threshold),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "accuracy": float(accuracy),
        "false_positive_rate": float(false_positive_rate),
        "true_positives": int(tp),
        "false_positives": int(fp),
        "true_negatives": int(tn),
        "false_negatives": int(fn),
    }


def collect_out_of_fold_scores(data):
    """
    Generate out-of-fold anomaly scores.

    Each record is scored by a model that was not trained on that record.
    Synthetic anomaly labels are used only for evaluation.
    """

    X = data[FEATURE_COLUMNS].copy()
    y = data["anomaly_label"].astype(int).to_numpy()

    if set(np.unique(y)) != {0, 1}:
        raise ValueError(
            "anomaly_label must contain both 0 (normal) and 1 (anomaly)."
        )

    cv = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    out_of_fold_scores = np.full(len(data), np.nan)

    for fold_number, (train_indices, test_indices) in enumerate(
        cv.split(X, y),
        start=1,
    ):
        X_train = X.iloc[train_indices]
        X_test = X.iloc[test_indices]

        # Fit imputation only on the training fold.
        imputer = SimpleImputer(strategy="median")

        X_train_imputed = imputer.fit_transform(X_train)
        X_test_imputed = imputer.transform(X_test)

        model = IsolationForest(
            n_estimators=200,
            contamination=0.03,
            max_samples=0.8,
            max_features=0.8,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

        # The model is trained without anomaly labels.
        model.fit(X_train_imputed)

        # Lower score_samples values indicate more anomalous records.
        scores = model.score_samples(X_test_imputed)

        out_of_fold_scores[test_indices] = scores

        print(
            f"Completed fold {fold_number}/3 "
            f"({len(test_indices)} records)"
        )

    if np.isnan(out_of_fold_scores).any():
        raise RuntimeError(
            "Some records did not receive out-of-fold scores."
        )

    return y, out_of_fold_scores


def tune_thresholds(y_true, anomaly_scores):
    """Evaluate multiple thresholds and select the best F1 score."""

    results = []

    for quantile in THRESHOLD_QUANTILES:
        threshold = np.quantile(
            anomaly_scores,
            quantile,
        )

        result = evaluate_threshold(
            y_true,
            anomaly_scores,
            threshold,
        )

        result["threshold_quantile"] = float(quantile)

        results.append(result)

    results.sort(
        key=lambda item: item["f1_score"],
        reverse=True,
    )

    return results


def main():
    print("Loading telemetry dataset...")

    data = load_dataset()

    print(f"Total records: {len(data)}")

    print("\nGenerating out-of-fold anomaly scores...")

    y_true, anomaly_scores = collect_out_of_fold_scores(data)

    print("\nEvaluating threshold candidates...")

    results = tune_thresholds(
        y_true,
        anomaly_scores,
    )

    best_result = results[0]

    output = {
        "experiment": "Isolation Forest threshold optimization",
        "evaluation_method": "3-fold stratified out-of-fold evaluation",
        "training_method": "Unsupervised Isolation Forest",
        "labels_used_for_training": False,
        "feature_columns": FEATURE_COLUMNS,
        "records_evaluated": len(data),
        "normal_records": int(np.sum(y_true == 0)),
        "anomaly_records": int(np.sum(y_true == 1)),
        "best_threshold": best_result,
        "all_threshold_results": results,
        "note": (
            "Thresholds were evaluated using synthetic anomaly labels. "
            "Results are experimental and do not represent clinical "
            "validation or real astronaut health performance."
        ),
    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            output,
            file,
            indent=4,
        )

    print("\nThreshold optimization completed.")

    print("\nBest threshold result:")
    print(json.dumps(best_result, indent=4))

    print(f"\nResults saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()