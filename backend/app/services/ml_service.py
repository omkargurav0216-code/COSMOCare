"""Integration adapter. The ML developer owns the code at ML_SRC_PATH."""
import sys
import importlib
from pathlib import Path

try:
    from app.core.config import settings
except (ImportError, ModuleNotFoundError):
    _backend_root = str(Path(__file__).resolve().parents[2])
    if _backend_root not in sys.path:
        sys.path.insert(0, _backend_root)
    from app.core.config import settings

FIELDS = (
    "astronaut_id",
    "timestamp",
    "heart_rate_bpm",
    "spo2_percent",
    "sleep_hours_last_24h",
    "body_temperature_celsius",
    "radiation_dose_rate_usv_per_hour",
    "activity_level_percent",
    "fatigue_level_0_10",
)

def _load():
    candidate_paths = [
        Path(settings.ML_SRC_PATH),
        (Path(__file__).resolve().parents[2] / settings.ML_SRC_PATH),
        (Path(__file__).resolve().parents[3] / "ml" / "src"),
        (Path(__file__).resolve().parents[2] / "ml" / "src"),
        (Path(__file__).resolve().parents[3] / "COSMOCare-ml-model" / "ml" / "src"),
    ]
    resolved_path = None
    for candidate in candidate_paths:
        try:
            cand = candidate.resolve()
            if cand.is_dir():
                resolved_path = cand
                break
        except Exception:
            continue

    if resolved_path is None:
        raise ImportError(
            f"ML source directory not found. Checked: {[str(c) for c in candidate_paths]}. Set ML_SRC_PATH in .env"
        )
    if str(resolved_path) not in sys.path:
        sys.path.insert(0, str(resolved_path))

    try:
        baseline_module = importlib.import_module("baseline.baseline")
        risk_engine_module = importlib.import_module("risk_assessment.risk_engine")
        calc_baseline = getattr(baseline_module, "calculate_baseline")
        calc_risk = getattr(risk_engine_module, "calculate_risk")
    except (ImportError, AttributeError) as exc:
        raise ImportError(f"Error loading ML functions from {resolved_path}: {exc}") from exc

    return calc_baseline, calc_risk

def calculate_baseline(history, min_history=24):
    calc_b, _ = _load()
    return calc_b(history, min_history=min_history)

def calculate_risk(telemetry, baseline, history=None, weights=None):
    _, calc_r = _load()
    return calc_r(telemetry, baseline, history=history, weights=weights)

def _records(rows):
    return [{key: getattr(row, key) for key in FIELDS} for row in rows]

def _score(astronaut_id, current, history):
    calc_b, calc_r = _load()
    baseline_records = _records(history)
    if not baseline_records:
        raise ValueError("At least one historical telemetry reading is required")
    baseline = calc_b(baseline_records, min_history=24)
    return calc_r(current, baseline, history=baseline_records)

def analyze(current, history):
    current_dict = {key: getattr(current, key) for key in FIELDS}
    return _score(current.astronaut_id, current_dict, history)

def analyze_simulation(astronaut_id, metrics, history):
    latest = {key: getattr(history[-1], key) for key in FIELDS}
    latest.update(metrics)
    latest["astronaut_id"] = astronaut_id
    # Historical baseline excludes the current reading when possible.
    baseline_history = history[:-1] if len(history) > 1 else history
    return _score(astronaut_id, latest, baseline_history)
