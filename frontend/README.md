
# Frontend – COSMOCare

The frontend module provides the interactive user interface for COSMOCare, enabling users to monitor astronaut health indicators, visualize health trends, review alerts, and interact with the AI health assistant.

## Technology Stack

- React
- Vite
- JavaScript (JSX)
- Tailwind CSS
- Recharts
- Lucide React

## Responsibilities

- Develop the main dashboard.
- Display astronaut profiles and health information.
- Visualize physiological metrics and historical trends.
- Display risk scores and anomaly alerts.
- Develop the AI chatbot interface.
- Integrate frontend components with backend APIs.
- Ensure responsive and user-friendly UI.

## Suggested Structure

```text
frontend/
│
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   ├── pages/
│   ├── layouts/
│   ├── hooks/
│   ├── services/
│   ├── context/
│   ├── utils/
│   ├── App.jsx
│   └── main.jsx
│
├── index.html
├── package.json
└── vite.config.js
```

## Backend Integration

The frontend communicates with the FastAPI backend through REST APIs.

Configure the backend URL using an environment variable:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Module Status

Under Development.
