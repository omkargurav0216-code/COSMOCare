# COSMOCare ML — Phase 6: Radiation Exposure Assessment

This phase estimates accumulated radiation dose over observed telemetry
intervals and calculates an experimental indicator by comparing the current
dose rate with the same astronaut's historical dose-rate mean.

## Files

- `ml/src/risk_assessment/radiation.py` — `calculate_radiation_risk(...)`.
- `ml/src/risk_assessment/__init__.py` — exports cardiovascular, fatigue,
  and radiation indicator functions.
- `tests/test_radiation.py` — unit tests.

## Example

```python
from ml.src.risk_assessment import calculate_radiation_risk

result = calculate_radiation_risk(
    telemetry=current_record,
    history=historical_records,
)
```

The current record must contain `astronaut_id`, `timestamp`, and
`radiation_dose_rate_usv_per_hour`. The current measurement can be flat or
inside a nested `metrics` object. History must contain those same three
columns. Only history for the current astronaut is used for their baseline
and dose integration.

## Dose versus dose rate

- Input: `radiation_dose_rate_usv_per_hour` in µSv/hour (dose rate).
- Output: `accumulated_dose_usv` in µSv (estimated accumulated dose).

The module uses trapezoidal integration between adjacent valid observations.
It assumes a linear change in dose rate between readings. Gaps longer than
`max_gap_hours` (default 2 hours) are skipped rather than extrapolated.
Therefore, the output covers only observed intervals and is not a lifetime
or mission-total exposure value.

## Experimental relative-rate indicator

- Compares the current dose rate with the astronaut's historical mean dose rate.
- A current rate 2x the historical mean maps to 100 points by default.
- The ratio threshold is configurable.
- If a positive historical mean is unavailable, the score is `None` and
  category is `insufficient_data`.
- Category bands: low (0–24.99), moderate (25–49.99),
  elevated (50–74.99), high (75–100).

This is a relative software-demo indicator only. No NASA radiation limit,
medical threshold, or mission safety threshold is invented or applied.
The ratio threshold and category bands are prototype assumptions.

## Run tests

From the repository root, with the ML virtual environment activated:

```cmd
python -m pip install pytest
python -m pytest tests
```

## Try with the current synthetic CSV

Run from the repository root after adding this phase:

```cmd
python -c "import pandas as pd; from ml.src.risk_assessment import calculate_radiation_risk; df=pd.read_csv('ml/data/raw/astronaut_telemetry.csv'); astro=df[df['astronaut_id']=='ASTRO_001'].sort_values('timestamp'); row=astro.iloc[-1].to_dict(); history=astro.iloc[:-1]; print(calculate_radiation_risk(row, history))"
```

## Integration note

The team's `docs/api-contracts.md` has not yet been published. This phase
returns an internal Python result and does not define a backend API schema.
Coordinate the eventual response shape with the backend developer.
