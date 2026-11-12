"""
ML integration package for COSMOCare backend.
Provides direct access to ML functions while delegating implementation to the ML module.
"""
from app.services.ml_service import (
    calculate_baseline,
    calculate_risk,
    analyze,
    analyze_simulation,
)

__all__ = [
    "calculate_baseline",
    "calculate_risk",
    "analyze",
    "analyze_simulation",
]
