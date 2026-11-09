
# AI Health Assistant – COSMOCare

The AI Health Assistant is the conversational intelligence module of COSMOCare. It enables users to interact with the system through natural language and obtain contextual information about astronaut health metrics, detected anomalies, risk assessments, and system insights.

## Technology Stack

- Python    MENTION PYTHON VERSION
- Large Language Model (LLM) API
- FastAPI integration
- REST APIs
- Prompt Engineering

Additional frameworks or retrieval techniques may be introduced depending on implementation requirements.

## Responsibilities

- Develop the conversational AI assistant.
- Integrate an LLM API.
- Design system prompts and conversation workflows.
- Retrieve relevant astronaut health information through approved backend interfaces.
- Explain risk assessment results in understandable language.
- Provide contextual responses based on available system data.
- Integrate chatbot functionality with the frontend.

## Core Capabilities

- Natural language interaction.
- Health metric explanations.
- Anomaly and alert explanations.
- Context-aware responses.
- Health trend summaries.
- General spaceflight health information.

## Suggested Structure

```text
ai-chatbot/
│
├── app/
│   ├── prompts/
│   ├── services/
│   ├── integrations/
│   ├── schemas/
│   └── main.py
│
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Navigate to chatbot directory

```bash
cd ai-chatbot
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

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file:

```env
LLM_API_KEY=your_api_key_here
```

Never commit actual credentials.

## Integration

The AI assistant communicates with the backend to retrieve authorized health information and provide contextual responses to the frontend.

It should distinguish between:
- Observed health measurements.
- Machine learning predictions.
- General informational guidance.

The assistant must not present model predictions as confirmed diagnoses or independently prescribe medical treatment.

## Module Status

Under Development.
