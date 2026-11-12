# COSMOCare Backend

FastAPI + SQLAlchemy + SQLite backend for COSMOCare. Built as the `backend` branch deliverable and organized by phases in [docs/PHASES.md](docs/PHASES.md).

## Requirements
Python 3.12.10. The ML repository additionally requires its own packages; install the combined backend requirements below.

## Setup (Windows PowerShell)
```powershell
cd COSMOCare-backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Set `ML_SRC_PATH` in `.env` to the ML repo's `ml/src` directory. Example when backend and ML directories are siblings:
`ML_SRC_PATH=../COSMOCare-ml-model/ml/src`

## Run
```bash
uvicorn app.main:app --reload
```
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- API base: http://localhost:8000/api/v1

SQLite file is created at `cosmocare.db`. Demo seed data is enabled by default; set `SEED_DATABASE=false` to disable it.

## Endpoints
| Method | Path |
|---|---|
| GET | `/api/v1/astronauts` |
| GET | `/api/v1/astronauts/{astronaut_id}` |
| GET | `/api/v1/astronauts/{astronaut_id}/telemetry` |
| POST | `/api/v1/telemetry` |
| GET | `/api/v1/astronauts/{astronaut_id}/risk` |
| POST | `/api/v1/astronauts/{astronaut_id}/risk/analyze` |
| GET | `/api/v1/astronauts/{astronaut_id}/alerts` |
| GET | `/api/v1/alerts` |
| PATCH | `/api/v1/alerts/{alert_id}` |
| POST | `/api/v1/simulation/run` |
| POST | `/api/v1/chat` |
| GET | `/health` |

## Test
```bash
python -m pytest -q
```

## Python version check

```powershell
python --version
# Expected: Python 3.12.10
```

## Integration notes
- Frontend base URL: `VITE_API_BASE_URL=http://localhost:8000/api/v1`.
- CORS origins are comma-separated in `CORS_ORIGINS`.
- ML implementation remains owned by the ML developer. This backend calls the published `ml/src` functions and does not duplicate them.
- Chat endpoint is an integration contract only. AI provider integration is pending and owned by the AI developer.
- Demo readings and risk thresholds are illustrative, not clinical guidance.
- Do not commit `.env`, credentials, database files or real astronaut personal data.

## Integration verification
The ML adapter uses the external ML repository's `calculate_baseline` and `calculate_risk` functions. Extract the ML ZIP alongside this backend and set `ML_SRC_PATH` to its `ml/src` folder. Risk endpoints return HTTP 503 if that folder is missing.

This package does not contain the AI provider implementation. Do not use prototype risk scores for clinical decisions.
