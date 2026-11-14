# COSMOCare AI Health Assistant

The **COSMOCare AI Health Assistant** is the conversational intelligence module of COSMOCare – Astronaut Health Monitoring & Risk Assessment System.

It enables users to interact with the platform through natural language and receive contextual explanations of astronaut health metrics, machine-learning risk assessments, anomalies, alerts, and general spaceflight health information.

The service uses **Google Gemini as its primary LLM provider and Groq as its fallback provider**, ensuring provider flexibility and improved service availability.

## Technology Stack

- **Language:** Python 3.12.10
- **Framework:** FastAPI
- **Primary LLM Provider:** Google Gemini API
- **Fallback LLM Provider:** GroqCloud API
- **LLM SDKs:** `google-genai`, `groq`
- **Environment Management:** python-dotenv
- **API Communication:** REST APIs
- **Server:** Uvicorn
- **Data Validation:** Pydantic

## Responsibilities

- Develop and maintain the conversational AI assistant.
- Integrate and manage LLM providers.
- Design system prompts and conversation workflows.
- Receive astronaut health context through approved backend interfaces.
- Explain health metrics, anomalies, alerts, and risk assessment results.
- Maintain contextual conversations using conversation history.
- Provide general, evidence-based spaceflight health information.
- Communicate with the main COSMOCare backend through authenticated internal APIs.

## Core Capabilities

- **Natural Language Interaction:** Answer user queries through conversational interfaces.
- **Health Metric Explanations:** Explain available astronaut telemetry and health indicators.
- **Risk Assessment Explanations:** Interpret machine-learning risk scores and predictions when supplied by the backend.
- **Alert Explanations:** Explain recorded alerts and their recommendations.
- **Context-Aware Responses:** Use astronaut-specific health information supplied by the backend.
- **Conversation History:** Maintain conversational context across messages.
- **Provider Fallback:** Use Groq when Gemini encounters a supported temporary failure.
- **General Health Information:** Provide informational guidance related to astronaut health and spaceflight.

## AI Provider Architecture

The service implements a primary–fallback provider architecture.

| Provider | Role | Model |
|---|---|---|
| Google Gemini | Primary | Configured through `GEMINI_MODEL` |
| GroqCloud | Fallback | `openai/gpt-oss-20b` by default |

### Request Workflow

1. The main COSMOCare backend sends a request to the AI service.
2. The AI service validates the internal authentication token.
3. The provider orchestrator attempts response generation using Gemini.
4. If Gemini encounters a supported temporary failure, the request is forwarded to Groq.
5. The generated response and selected model information are returned to the main backend.
6. The backend handles conversation persistence and returns the response to the frontend.

**Note:** Automatic fallback is implemented but has not yet been verified through a live Gemini failure test.

## Integration Architecture

The AI service operates independently from the main COSMOCare backend.

- The main backend manages the database, conversations, messages, and astronaut health context.
- The AI service handles LLM communication and response generation.
- The frontend communicates with the main backend rather than calling external LLM APIs directly.
- Internal service communication is protected using an `X-Internal-Token` header.

### Internal API Endpoint

`POST /internal/generate`

The endpoint accepts:
- User message
- Optional astronaut health context
- Recent conversation history

The response contains:
- Generated answer
- Model used for generation

## Project Structure

```text
ai-chatbot/
│
├── app/
│   ├── prompts/
│   │   └── __init__.py
│   │
│   ├── routes/
│   │   └── chat.py
│   │
│   ├── schemas/
│   │   └── chat.py
│   │
│   ├── services/
│   │   └── llm_client.py
│   │
│   ├── config.py
│   └── main.py
│
├── .env
├── .env.example
├── .python-version
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Navigate to the AI service directory

```bash
cd ai-chatbot
```

### 2. Create a virtual environment

Python 3.12.10 is required.

```bash
py -3.12 -m venv .venv
```

### 3. Activate the virtual environment

**Windows – Git Bash:**

```bash
source .venv/Scripts/activate
```

**Windows – Command Prompt:**

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file inside the `ai-chatbot` directory.

```env
# Gemini - Primary Provider
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash

# Groq - Fallback Provider
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
GROQ_TIMEOUT=45

# Internal API Authentication
INTERNAL_API_TOKEN=your_shared_internal_token
```

**Important:**
- Generate API keys from the respective provider dashboards.
- The internal API token must match the token configured in the main backend.
- Never commit `.env` files or expose API credentials.
- Refer to `.env.example` for the configuration template.

### 6. Run the AI service

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 9000
```

The service will be available at:

- Base URL: `http://127.0.0.1:9000`
- API documentation: `http://127.0.0.1:9000/docs`

## Integration with COSMOCare Backend

The AI service runs independently on port `9000`, while the main backend runs on port `8000`.

Configure the following environment variables in the main backend:

```env
AI_SERVICE_URL=http://127.0.0.1:9000
INTERNAL_API_TOKEN=your_shared_internal_token
AI_SERVICE_TIMEOUT=45
```

Both services must use the same internal API token.

## Safety and Responsible AI

The COSMOCare AI Assistant is an informational and decision-support component.

- It must not diagnose medical conditions.
- It must not prescribe medication or treatment.
- It must not invent astronaut measurements, alerts, or risk scores.
- It must distinguish observed telemetry from machine-learning predictions.
- It must not present experimental risk scores as confirmed medical diagnoses or official NASA safety determinations.
- It must communicate uncertainty and missing information.
- Urgent health concerns must be referred to qualified medical or mission health personnel.

The assistant's responses are intended to support human decision-making, not replace qualified medical professionals.

## Module Status

**Implemented – Integration and further testing ongoing.**

Current implementation includes:
- Gemini primary provider integration.
- Groq fallback provider integration.
- Authenticated internal API communication.
- Astronaut context and conversation history support.
- Integration with the main COSMOCare backend.
- Frontend conversational interface.

Automatic provider failover and production deployment require further verification.