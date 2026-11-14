# COSMOCare
### AI-Powered Astronaut Health Monitoring & Risk Assessment System

**COSMOCare** is an AI-powered astronaut health monitoring and risk assessment system developed as part of the **NASA Space Apps Challenge 2026**.

Designed to support astronaut well-being during long-duration space missions, COSMOCare combines health telemetry monitoring, machine learning, anomaly detection, explainable risk assessment, and an AI-powered conversational assistant to transform health data into meaningful insights.

The platform aims to help monitor astronaut health indicators, identify unusual patterns, assess potential health risks, generate alerts, and provide contextual information to support mission health personnel.

---

## Project Objectives

- Monitor astronaut health indicators using available telemetry data.
- Identify unusual health patterns and potential anomalies.
- Apply machine-learning models to assess health-related risks.
- Provide interpretable risk assessment results.
- Generate alerts based on configured risk thresholds.
- Provide an AI-powered assistant for explaining health metrics, alerts, and ML predictions.
- Support informed decision-making during long-duration space missions.

## Key Features

### 1. Astronaut Health Monitoring
- Display astronaut information and mission details.
- Monitor available health telemetry.
- Visualize health indicators through interactive dashboards.
- Track health measurements over time.

### 2. Machine Learning Risk Assessment
- Process health-related telemetry using machine-learning models.
- Estimate potential health risks.
- Generate risk assessment results.
- Support explainability and interpretation of model outputs.

### 3. Anomaly Detection
- Identify unusual patterns in available health measurements.
- Support anomaly identification through machine-learning techniques.
- Highlight potentially concerning observations for further review.

### 4. Alert Management
- Generate alerts based on configured thresholds and risk assessments.
- Display alert severity and descriptions.
- Provide recorded recommendations for review.

### 5. AI Health Assistant
- Natural-language interaction through the COSMOCare Assistant.
- Explain available astronaut health metrics.
- Explain machine-learning risk assessments and alerts.
- Provide astronaut-specific responses using backend-supplied context.
- Maintain conversation history.
- Use Google Gemini as the primary LLM provider and GroqCloud as the fallback provider for supported temporary failures.
- Render structured AI responses using Markdown.

---

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript |
| Styling | Tailwind CSS |
| Icons | Lucide React |
| Data Visualization | Recharts |
| Backend | Python 3.12.10, FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite |
| Data Validation | Pydantic |
| Machine Learning | Pandas, NumPy, Scikit-learn |
| Anomaly Detection | Isolation Forest |
| AI Assistant | Google Gemini API, GroqCloud API |
| AI Service Framework | FastAPI |
| AI SDKs | google-genai, groq |
| API Communication | REST APIs |
| Version Control | Git, GitHub |

## System Architecture

COSMOCare follows a modular architecture in which the frontend, backend, machine-learning module, and AI chatbot operate as separate components.

```text
                  COSMOCARE PLATFORM
                          |
          +---------------+---------------+
          |                               |
     React Frontend                  FastAPI Backend
          |                               |
          |                       +-------+-------+
          |                       |       |       |
          |                    Database   ML    AI Client
          |                       |       |       |
          |                       |    Risk      |
          |                       | Assessment   |
          |                       |              |
          |                       +--------------+
          |                              |
          |                       Independent AI Service
          |                              |
          |                     Provider Orchestrator
          |                              |
          |                      +-------+-------+
          |                      |               |
          |                    Gemini           Groq
          |                   Primary         Fallback
          |
          +---------- REST API Communication
```

### Component Responsibilities

**Frontend**
- Provides the user interface and astronaut dashboard.
- Displays telemetry, risk assessments, alerts, and assistant conversations.
- Communicates with the main backend through REST APIs.

**Backend**
- Manages application APIs and database operations.
- Retrieves astronaut information and telemetry.
- Integrates with the ML module.
- Generates and manages alerts.
- Retrieves astronaut-specific context for AI conversations.
- Stores conversation history and messages.
- Communicates with the independent AI service.

**Machine Learning Module**
- Processes available astronaut health data.
- Performs baseline calculations and risk assessments.
- Provides model-generated outputs to the backend.

**AI Chatbot**
- Processes natural-language questions.
- Explains available astronaut health information.
- Uses backend-supplied context and conversation history.
- Communicates with external LLM providers through a dedicated AI service.

---
## Project Structure

```text
COSMOCare/
│
├── frontend/       # User interface and dashboard
├── backend/        # FastAPI backend and APIs
├── ml/             # ML models and risk assessment
├── ai-chatbot/     # AI health assistant
├── docs/           # Documentation and architecture
│
├── README.md
├── .gitignore
└── LICENSE
```

---

## Installation and Setup

### Prerequisites

- Python 3.12.10
- Node.js and npm
- Git
- Gemini API key
- GroqCloud API key

### 1. Clone the repository

```bash
git clone https://github.com/omkargurav0216-code/COSMOCare.git
cd COSMOCare
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create and activate the virtual environment:

```bash
py -3.12 -m venv .venv
```

Windows – Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```bash
cp .env.example .env
```

Configure the required database, ML, and AI service settings in `.env`.

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend documentation:

http://localhost:8000/docs

### 3. AI Chatbot Setup

Open another terminal:

```bash
cd ai-chatbot
```

Create and activate the virtual environment:

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```bash
cp .env.example .env
```

Add the required Gemini, Groq, and internal authentication credentials to `.env`.

Start the AI service:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 9000
```

AI service documentation:

http://localhost:9000/docs

### 4. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend:

http://localhost:5173

---

## API Overview

The main backend exposes REST endpoints for astronaut management, telemetry, risk assessments, alerts, simulations, and chat.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/astronauts` | Retrieve astronauts |
| GET | `/api/v1/astronauts/{astronaut_id}` | Retrieve astronaut details |
| GET | `/api/v1/astronauts/{astronaut_id}/telemetry` | Retrieve telemetry |
| POST | `/api/v1/telemetry` | Submit telemetry |
| GET | `/api/v1/astronauts/{astronaut_id}/risk` | Retrieve risk assessment |
| POST | `/api/v1/astronauts/{astronaut_id}/risk/analyze` | Perform risk analysis |
| GET | `/api/v1/astronauts/{astronaut_id}/alerts` | Retrieve astronaut alerts |
| GET | `/api/v1/alerts` | Retrieve alerts |
| PATCH | `/api/v1/alerts/{alert_id}` | Update alert |
| POST | `/api/v1/simulation/run` | Run simulation |
| POST | `/api/v1/chat` | Send AI chat message |

For detailed endpoint documentation, run the backend and visit `/docs`.

---

## Team

Developed by a four-member team for the **NASA Space Apps Challenge 2026**.

| Branch | Assigned Role | Team Member |
|---|---|---|
| `frontend` | Frontend Development | [Mayur N Dharwadkar](https://github.com/Mayur-N-D) |
| `ml-model` | ML Model Development | [Pranay Patil](https://github.com/Pranay-Pandurang-Patil) |
| `backend` | Backend Development | [Mayur Shivaji Gawade](https://github.com/mayurshivajigawade) |
| `integration` | Integration & AI Chatbot | [Omkar Gurav](https://github.com/omkargurav0216-code) |

---

## Safety, Privacy and Limitations

COSMOCare is a research prototype and decision-support system.

- Machine-learning risk scores are statistical estimates, not confirmed medical diagnoses.
- AI-generated information is not a substitute for qualified medical personnel.
- Demo telemetry and risk thresholds are illustrative and should not be treated as clinical guidance.
- The system must not invent missing astronaut measurements or assessment results.
- API credentials and environment files must never be committed to Git.
- Real astronaut health data must not be sent to external AI providers without appropriate privacy, security, and data-handling approval.
- Proper authentication and astronaut-level authorization are required before public deployment or use with real health information.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

**COSMOCare — Keeping Astronauts Healthy, Beyond Earth.**