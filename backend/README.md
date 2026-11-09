
# Backend – COSMOCare

The backend module serves as the central communication layer of COSMOCare. It manages API requests, processes health data, coordinates machine learning predictions, and connects the frontend with the AI assistant.

## Technology Stack

- Python    MENTION PYTHON VERSION
- FastAPI
- Uvicorn
- Pydantic
- SQLite / PostgreSQL
- SQLAlchemy (if required)

## Responsibilities

- Develop REST API endpoints.
- Receive and process astronaut health data.
- Integrate machine learning predictions.
- Retrieve risk assessment results.
- Manage health alerts and records.
- Connect frontend services with the AI assistant.
- Handle database operations.

## Suggested Structure

```text
backend/
│
├── app/
│   ├── api/
│   │   └── routes/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── database/
│   └── main.py
│
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Navigate to backend

```bash
cd backend
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate environment

Windows:
```bash
venv\Scripts\activate
```

Linux / macOS:
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start FastAPI server

```bash
uvicorn app.main:app --reload
```

API documentation:

- Swagger UI: http://localhost:8000/docs

## API Responsibilities

The backend is expected to provide endpoints for:

- Health data retrieval.
- Astronaut profile management.
- Health risk assessment.
- Anomaly detection.
- Alert management.
- AI chatbot communication.

Exact endpoints and request/response schemas will be documented as implementation progresses.

## Environment Variables

Store sensitive configuration in `.env`.

Example:

```env
DATABASE_URL=
LLM_API_KEY=
```

Never commit actual API keys or credentials.

## Module Status

Under Development.
