# COSMOCare Backend

FastAPI + SQLAlchemy + SQLite backend for COSMOCare. Built as the `backend` branch deliverable and organized by phases in [docs/PHASES.md](docs/PHASES.md).

The COSMOCare backend is the central API and data-management layer of **COSMOCare – Astronaut Health Monitoring & Risk Assessment System**.

The backend also acts as the integration layer between the React frontend, ML module, database, and independent AI chatbot service.

## Requirements
- **Python:** 3.12.10
- **Server:** Uvicorn
- **Validation:** Pydantic

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

Configure the AI service integration variables as described in the AI Integration section.

## Run
```bash
uvicorn app.main:app --reload
```
The backend runs at `http://localhost:8000` by default.

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

## Integration Architecture

The backend connects the following components:

1. **Frontend:** React application communicates with the backend through REST APIs.
2. **Database:** SQLAlchemy manages astronaut records, telemetry, risk assessments, alerts, conversations, and messages.
3. **ML Module:** The backend invokes functions provided by the independent ML repository.
4. **AI Chatbot:** The backend forwards chat requests and relevant astronaut context to the independent AI service.

The backend remains responsible for database access, conversation persistence, and communication with the frontend.

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
The ML adapter uses the external ML repository's `calculate_baseline` and `calculate_risk` functions. Extract the ML ZIP alongside this backend and set `ML_SRC_PATH` to its `ml/src` folder. Risk endpoints return HTTP 503 if that folder is missing.'

### AI Integration

COSMOCare uses an independent FastAPI-based AI chatbot service.

1. The frontend sends a message to `POST /api/v1/chat`.
2. The backend validates the conversation and astronaut association.
3. The backend retrieves recent conversation history and available astronaut health context.
4. The user message is persisted.
5. The backend forwards the message, context, and history to the AI service.
6. The AI service generates a response using its configured LLM provider.
7. The backend saves the assistant response and returns it to the frontend.

### AI service configuration

Configure the following variables in the backend `.env`:

```env
AI_SERVICE_URL=http://127.0.0.1:9000
INTERNAL_API_TOKEN=your_shared_internal_token
AI_SERVICE_TIMEOUT=45
CHAT_MOCK_MODE=false

This package does not contain the AI provider implementation. Do not use prototype risk scores for clinical decisions.
