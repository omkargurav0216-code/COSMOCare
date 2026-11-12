# COSMOCare — Machine Learning Module

## 1. Overview

The COSMOCare Machine Learning module provides astronaut health telemetry preprocessing, individual baseline calculation, health-risk indicators, anomaly detection, and explainable risk assessment.

The module is designed to support health monitoring during long-duration space missions.

It processes astronaut telemetry, identifies unusual measurements, evaluates health indicators, and provides information that can support health-risk assessment.

**Important:** All datasets currently used for development and evaluation are synthetic. The model is an experimental decision-support component and is not clinically validated.

---

## 2. ML Module Objectives

The ML module implements the following capabilities:

1. Synthetic astronaut telemetry generation.
2. Telemetry preprocessing and validation.
3. Individual astronaut baseline calculation.
4. Cardiovascular risk assessment.
5. Fatigue risk assessment.
6. Radiation exposure assessment.
7. Overall health-risk calculation.
8. Isolation Forest anomaly detection.
9. Persistent trained model storage and inference.
10. Model evaluation and optimization.

---

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | ML development environment |
| NumPy | Numerical operations |
| Pandas | Telemetry processing |
| Scikit-learn | Machine learning and anomaly detection |
| Joblib | Persistent model serialization |
| Pytest | Automated testing |
| JSON | Evaluation metrics and experiment results |

---

## 4. Project Structure

```text
ml/
│
├── data/
│   ├── raw/
│   │   └── astronaut_telemetry.csv
│   │
│   ├── processed/
│   │
│   └── validation/
│       └── astronaut_validation.csv
│
├── models/
│   ├── isolation_forest.joblib
│   ├── evaluation_metrics.json
│   ├── optimization_results.json
│   ├── threshold_optimization_results.json
│   └── validation_metrics.json
│
├── notebooks/
│
├── src/
│   │
│   ├── preprocessing/
│   │   ├── generate_synthetic_data.py
│   │   ├── generate_validation_data.py
│   │   └── telemetry_preprocessing.py
│   │
│   ├── baseline/
│   │   └── baseline.py
│   │
│   ├── anomaly_detection/
│   │   ├── anomaly_detection.py
│   │   ├── train.py
│   │   ├── model_loader.py
│   │   ├── tune.py
│   │   ├── threshold_tuning.py
│   │   └── validate_model.py
│   │
│   ├── evaluation/
│   │
│   └── risk_assessment/
│       ├── cardiovascular.py
│       ├── fatigue.py
│       ├── radiation.py
│       └── risk_engine.py
│
├── tests/
│   ├── test_anomaly_detection.py
│   ├── test_baseline.py
│   ├── test_cardiovascular.py
│   ├── test_fatigue.py
│   ├── test_persistent_model.py
│   ├── test_radiation.py
│   ├── test_risk_engine.py
│   └── test_telemetry_preprocessing.py
│
├── requirements.txt
└── README.md
```

---

## 5. Synthetic Telemetry Dataset

The ML module uses synthetic astronaut telemetry for development and testing.

### Dataset configuration

| Parameter | Value |
|---|---:|
| Number of astronauts | 4 |
| Simulation duration | 14 days |
| Readings per day | 24 |
| Total records | 1,344 |
| Training random seed | 42 |
| Validation random seed | 2026 |

### Telemetry features

| Feature | Description |
|---|---|
| astronaut_id | Unique astronaut identifier |
| timestamp | Telemetry timestamp |
| heart_rate_bpm | Heart rate |
| spo2_percent | Blood oxygen saturation |
| sleep_hours_last_24h | Sleep duration |
| body_temperature_celsius | Body temperature |
| radiation_dose_rate_usv_per_hour | Radiation dose rate |
| activity_level_percent | Activity level |
| fatigue_level_0_10 | Fatigue indicator |
| anomaly_label | Synthetic anomaly label |
| anomaly_type | Simulated anomaly category |
| data_source | Dataset source |

### Synthetic anomaly categories

The generator introduces occasional unusual readings, including:

- Elevated heart rate
- Low SpO2
- Elevated body temperature
- High fatigue
- Elevated radiation dose rate

The synthetic anomaly labels are used for model evaluation, not as training features.

### Generate training data

From the repository root:

```cmd
set PYTHONPATH=D:\Projects\COSMOCare\ml\src

.\ml\venv312\Scripts\python.exe -m preprocessing.generate_synthetic_data
```

Output:

```text
ml/data/raw/astronaut_telemetry.csv
```

### Generate validation data

```cmd
.\ml\venv312\Scripts\python.exe -m preprocessing.generate_validation_data
```

Output:

```text
ml/data/validation/astronaut_validation.csv
```

The validation generator uses a different random seed to produce a separate synthetic dataset.

---

## 6. Telemetry Preprocessing

The preprocessing module prepares telemetry for downstream ML components.

Responsibilities include:

- Input validation.
- Timestamp normalization.
- Measurement validation.
- Handling missing values.
- Preserving missing measurements instead of replacing them with zero.
- Generating warnings for invalid measurements.

The preprocessing module supports structured telemetry input and prepares the data for baseline calculations, risk assessment, and anomaly detection.

---

## 7. Individual Baseline Calculation

The baseline module calculates individual astronaut reference statistics from historical telemetry.

Individual baselines help distinguish normal variations from unusual changes in an astronaut's measurements.

Baselines are calculated separately for each astronaut.

This supports personalized health monitoring instead of relying exclusively on one common reference profile.

---

## 8. Health-Risk Assessment

The risk-assessment module contains three primary indicators.

### 8.1 Cardiovascular Risk

Evaluates cardiovascular-related telemetry measurements against individual baseline information.

### 8.2 Fatigue Risk

Evaluates fatigue-related measurements, including sleep duration and fatigue indicators.

### 8.3 Radiation Risk

Evaluates radiation dose-rate information and historical radiation exposure.

Radiation dose rate and accumulated radiation dose are treated as separate concepts.

### 8.4 Overall Risk Engine

The risk engine combines available component indicators into an overall risk assessment.

It supports configurable weights and handles unavailable indicators without automatically treating missing information as zero.

---

## 9. Anomaly Detection

COSMOCare uses the Isolation Forest algorithm from Scikit-learn.

Isolation Forest is an unsupervised anomaly-detection algorithm that identifies observations that differ from the learned data distribution.

The implementation supports:

- Historical telemetry analysis.
- Unusual measurement detection.
- Persistent model training.
- Model serialization.
- Reusable inference.
- Evaluation and parameter optimization.

### Selected model configuration

| Parameter | Value |
|---|---:|
| Algorithm | Isolation Forest |
| Model version | 1.1.0 |
| Number of estimators | 200 |
| Contamination | 0.03 |
| Maximum samples | 0.8 |
| Maximum features | 0.8 |
| Random state | 42 |

### Model features

The persistent model uses seven telemetry features:

1. Heart rate
2. SpO2
3. Sleep duration
4. Body temperature
5. Radiation dose rate
6. Activity level
7. Fatigue level

### Selected anomaly threshold

```text
-0.5216710512408959
```

The threshold was selected through out-of-fold threshold optimization.

Lower Isolation Forest `score_samples()` values indicate more anomalous observations.

Predictions use the selected threshold consistently during evaluation and inference.

---

## 10. Persistent Model Training

The persistent training implementation is located at:

```text
ml/src/anomaly_detection/train.py
```

The training workflow:

1. Loads historical telemetry.
2. Applies telemetry preprocessing.
3. Extracts the seven model features.
4. Fits the missing-value imputer using training data.
5. Trains the Isolation Forest model.
6. Evaluates the model using the separate validation dataset.
7. Saves the trained pipeline and threshold using Joblib.
8. Saves evaluation metrics in JSON format.

Anomaly labels are deliberately excluded from model training.

### Train the model

From the repository root, use CMD:

```cmd
set PYTHONPATH=D:\Projects\COSMOCare

.\ml\venv312\Scripts\python.exe -m ml.src.anomaly_detection.train
```

### Generated model artifact

```text
ml/models/isolation_forest.joblib
```

The saved artifact contains:

- Trained preprocessing and Isolation Forest pipeline.
- Feature column definitions.
- Selected anomaly threshold.
- Model metadata.
- Model version.

The backend can load and reuse this artifact without retraining on every request.

---

## 11. Model Loading and Inference

The model-loading implementation is located at:

```text
ml/src/anomaly_detection/model_loader.py
```

Main functions:

```python
load_anomaly_model()
```

Loads the persisted model artifact.

```python
predict_anomaly(data, artifact)
```

Performs anomaly inference for a single telemetry record.

### Inference workflow

1. Load the trained model artifact.
2. Receive a telemetry record.
3. Extract the expected features.
4. Apply the fitted imputer.
5. Calculate the Isolation Forest anomaly score.
6. Compare the score with the persisted threshold.
7. Return the anomaly result.

The inference function does not train or refit the model.

### Example usage

```python
from ml.src.anomaly_detection.model_loader import (
    load_anomaly_model,
    predict_anomaly,
)

artifact = load_anomaly_model()

telemetry = {
    "heart_rate_bpm": 80,
    "spo2_percent": 97,
    "sleep_hours_last_24h": 7,
    "body_temperature_celsius": 36.8,
    "radiation_dose_rate_usv_per_hour": 0.3,
    "activity_level_percent": 60,
    "fatigue_level_0_10": 4,
}

result = predict_anomaly(telemetry, artifact)

print(result)
```

### Example response structure

```json
{
    "status": "available",
    "is_anomaly": false,
    "anomaly_score": 0.25,
    "decision_threshold": -0.5216710512408959,
    "model_version": "1.1.0",
    "features_used": [
        "heart_rate_bpm",
        "spo2_percent",
        "sleep_hours_last_24h",
        "body_temperature_celsius",
        "radiation_dose_rate_usv_per_hour",
        "activity_level_percent",
        "fatigue_level_0_10"
    ],
    "warnings": [
        "Statistical anomaly flag; not a clinical diagnosis."
    ]
}
```

The numerical anomaly score above is illustrative, not an actual prediction output.

---

## 12. Model Optimization

The optimization implementation is located at:

```text
ml/src/anomaly_detection/tune.py
```

It evaluates multiple Isolation Forest configurations using stratified cross-validation.

The experiment compares:

- Number of estimators.
- Contamination.
- Maximum samples.
- Maximum features.

Evaluation metrics include:

- Precision.
- Recall.
- F1-score.
- False positive rate.
- Confusion matrix.

### Run hyperparameter optimization

```cmd
set PYTHONPATH=D:\Projects\COSMOCare\ml\src

.\ml\venv312\Scripts\python.exe -m anomaly_detection.tune
```

Results:

```text
ml/models/optimization_results.json
```

The optimization experiment does not overwrite the production model.

---

## 13. Threshold Optimization

The threshold optimization implementation is located at:

```text
ml/src/anomaly_detection/threshold_tuning.py
```

It evaluates multiple score thresholds using out-of-fold Isolation Forest scores.

The objective is to examine the balance between:

- Precision.
- Recall.
- F1-score.
- Accuracy.
- False positive rate.

### Run threshold optimization

```cmd
.\ml\venv312\Scripts\python.exe -m anomaly_detection.threshold_tuning
```

Results:

```text
ml/models/threshold_optimization_results.json
```

The selected threshold is evaluated separately on the independent synthetic validation dataset.

---

## 14. Independent Model Validation

The validation implementation is located at:

```text
ml/src/anomaly_detection/validate_model.py
```

The script:

1. Loads the original training dataset.
2. Loads the separate validation dataset.
3. Trains the optimized Isolation Forest on training data only.
4. Applies the selected threshold.
5. Evaluates predictions against synthetic validation labels.
6. Saves evaluation metrics.

### Run validation

```cmd
.\ml\venv312\Scripts\python.exe -m anomaly_detection.validate_model
```

Output:

```text
ml/models/validation_metrics.json
```

### Independent validation results

| Metric | Result |
|---|---:|
| Validation records | 1,344 |
| Normal records | 1,303 |
| Anomaly records | 41 |
| Precision | 75.00% |
| Recall | 80.49% |
| F1-score | 77.65% |
| Accuracy | 98.59% |
| False positive rate | 0.84% |

### Confusion matrix

| Actual / Predicted | Normal | Anomaly |
|---|---:|---:|
| Normal | 1,292 | 11 |
| Anomaly | 8 | 33 |

These metrics describe performance on independently generated synthetic telemetry. They do not establish real-world astronaut health-monitoring performance.

---

## 15. Model Evaluation Artifacts

The following artifacts are generated during training and experimentation.

| File | Description |
|---|---|
| `isolation_forest.joblib` | Persistent trained model |
| `evaluation_metrics.json` | Final training and validation metrics |
| `optimization_results.json` | Hyperparameter optimization results |
| `threshold_optimization_results.json` | Threshold experiment results |
| `validation_metrics.json` | Independent validation results |

---

## 16. Installation and Environment Setup

Recommended development environment:

- Python 3.12
- Windows CMD or PowerShell
- Virtual environment

Create the virtual environment from the repository root:

```cmd
py -3.12 -m venv ml\venv312
```

Activate it:

```cmd
ml\venv312\Scripts\activate
```

Install dependencies:

```cmd
python -m pip install -r ml\requirements.txt
```

Install pytest if it is not already included:

```cmd
python -m pip install pytest
```

---

## 17. Automated Testing

The ML module contains automated tests for:

- Telemetry preprocessing.
- Individual baseline calculations.
- Cardiovascular risk.
- Fatigue risk.
- Radiation assessment.
- Overall risk calculation.
- Anomaly detection.
- Persistent model loading and inference.

### Run the complete test suite

From the repository root:

```cmd
set PYTHONPATH=D:\Projects\COSMOCare\ml\src

.\ml\venv312\Scripts\python.exe -m pytest .\ml\tests\ -v
```

### Latest test status

```text
76 passed
```

All 76 ML tests passed during the latest verification.

---

## 18. Backend Integration

COSMOCare follows a modular monolith architecture.

The ML module is designed to be imported directly by the FastAPI backend.

The backend is responsible for API endpoints and request/response handling.

The ML module provides reusable Python functions for:

- Telemetry preprocessing.
- Baseline calculation.
- Risk assessment.
- Anomaly detection.
- Explanation generation.

The persistent anomaly model should be loaded once and reused by the backend rather than retrained for every incoming request.

The ML module does not operate as a separate ML API server.

---

## 19. Important Limitations

- All current telemetry datasets are synthetic.
- Synthetic labels represent simulated anomalies, not confirmed medical conditions.
- Model evaluation metrics do not establish clinical accuracy.
- The selected threshold is based on synthetic-data experiments.
- The model is not validated for actual astronaut medical decision-making.
- Risk indicators are decision-support outputs, not medical diagnoses.
- Real mission deployment would require appropriate validated datasets, domain review, and safety assessment.

---

## 20. Future Improvements

Potential future improvements include:

- Evaluation using additional representative telemetry scenarios.
- More robust anomaly detection.
- Additional model evaluation and monitoring.
- Improved explainability of anomaly results.
- Integration with backend telemetry APIs.
- Testing with realistic mission-specific simulation data.
- Evaluation of model stability across different astronaut profiles.

---

## 21. Project Summary

The COSMOCare ML module provides a modular machine-learning foundation for astronaut health monitoring.

It combines telemetry preprocessing, individual baselines, health-risk indicators, Isolation Forest anomaly detection, persistent model storage, and automated testing.

The current implementation has:

- Seven anomaly-detection features.
- A persistent Isolation Forest model.
- Reusable inference functionality.
- Hyperparameter and threshold optimization experiments.
- Independent synthetic validation.
- 76 passing automated tests.

**COSMOCare aims to support astronaut health monitoring through explainable, data-driven decision support.**