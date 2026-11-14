# COSMOCare Backend API Contract

**API version:** v1
**Base URL (local):** `http://localhost:8000`
**API prefix:** `/api/v1`
**Interactive API documentation:** `/docs`

## 1. Overview

The COSMOCare backend provides APIs for astronaut information, health telemetry, risk assessment, alerts, hypothetical simulations and AI chat handoff.

All request and response bodies use JSON unless otherwise specified.

## 2. Endpoint Summary

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Backend health check |
| GET | `/api/v1/astronauts` | List astronauts |
| GET | `/api/v1/astronauts/{astronaut_id}` | Get astronaut details |
| GET | `/api/v1/astronauts/{astronaut_id}/telemetry` | Get telemetry history |
| POST | `/api/v1/telemetry` | Submit telemetry |
| GET | `/api/v1/astronauts/{astronaut_id}/risk` | Get risk assessment history |
| POST | `/api/v1/astronauts/{astronaut_id}/risk/analyze` | Run risk analysis |
| GET | `/api/v1/alerts` | List alerts |
| GET | `/api/v1/astronauts/{astronaut_id}/alerts` | Get astronaut alerts |
| PATCH | `/api/v1/alerts/{alert_id}` | Update alert status |
| POST | `/api/v1/simulation/run` | Run hypothetical simulation |
| POST | `/api/v1/chat` | Save a chat message and hand off to AI integration |

## 3. Astronaut APIs

### GET `/api/v1/astronauts`

Returns all astronauts, ordered by astronaut ID.

Example response:

```json
[
  {
    "id": "AST-001",
    "name": "Alex Morgan",
    "role": "Mission Commander",
    "mission": "ASTRA-01",
    "age": 42,
    "status": "Active"
  }
]
```

### GET `/api/v1/astronauts/{astronaut_id}`

Returns details for one astronaut.

Possible error:
- `404`: Astronaut not found.

## 4. Telemetry APIs

### GET `/api/v1/astronauts/{astronaut_id}/telemetry`

Returns telemetry history, newest records first.

Query parameter:

| Parameter | Type | Default | Behavior |
|---|---|---|---|
| `limit` | Integer | 100 | Clamped between 1 and 1000 |

Possible error:
- `404`: Astronaut not found.

### POST `/api/v1/telemetry`

Submits a telemetry record and saves it to the database.

Example request:

```json
{
  "astronaut_id": "AST-001",
  "heart_rate_bpm": 74,
  "spo2_percent": 98,
  "sleep_hours_last_24h": 7.5,
  "body_temperature_celsius": 36.8,
  "radiation_dose_rate_usv_per_hour": 0.44,
  "activity_level_percent": 54,
  "fatigue_level_0_10": 2
}
```

The `timestamp` field is optional and defaults to the current UTC time.

Validation limits:

| Field | Accepted range | Unit |
|---|---:|---|
| `heart_rate_bpm` | 0Ã¢â‚¬â€œ300 | BPM |
| `spo2_percent` | 0Ã¢â‚¬â€œ100 | % |
| `sleep_hours_last_24h` | 0Ã¢â‚¬â€œ24 | Hours |
| `body_temperature_celsius` | 25Ã¢â‚¬â€œ45 | Ã‚Â°C |
| `radiation_dose_rate_usv_per_hour` | 0 or greater | ÃŽÂ¼Sv/hour |
| `activity_level_percent` | 0Ã¢â‚¬â€œ100 | % |
| `fatigue_level_0_10` | 0Ã¢â‚¬â€œ10 | Scale |

All health metric fields are optional and may be null.

**Important:** Heart-rate values below 20 or above 250 receive an `unusual_heart_rate_bpm` quality warning. Such values are still accepted and saved if they pass the schema's 0Ã¢â‚¬â€œ300 validation.

Successful response: `201 Created`, with the saved telemetry record, its database ID and `quality_warnings`.

Possible errors:
- `404`: Astronaut not found.
- `422`: Request validation failure.

## 5. Risk Assessment APIs

### GET `/api/v1/astronauts/{astronaut_id}/risk`

Returns the astronaut's latest 100 risk assessments, newest first.

The response is an array, not a single object.

Each assessment includes:

- `id`
- `astronaut_id`
- `score`
- `category`
- `status`
- `result`
- `created_at`

The `result` object contains detailed indicator scores, components, explanations, weights, warnings, model version and limitations.

### POST `/api/v1/astronauts/{astronaut_id}/risk/analyze`

Runs the ML risk engine using the astronaut's available telemetry history.

The assessment is saved in the database. Applicable indicator alerts are generated.

Possible errors:
- `404`: Astronaut not found.
- `422`: Insufficient telemetry or risk calculation input error.
- `503`: ML module unavailable.

**Risk interpretation:** Scores and categories are experimental software indicators. They are not medical diagnoses or NASA safety determinations.

## 6. Alert APIs

### GET `/api/v1/alerts`

Returns the latest 500 alerts.

Optional query parameter:

`status` Ã¢â‚¬â€ filters alerts by their exact status string.

### GET `/api/v1/astronauts/{astronaut_id}/alerts`

Returns all alerts for the specified astronaut, newest first.

Possible error:
- `404`: Astronaut not found.

### PATCH `/api/v1/alerts/{alert_id}`

Updates an alert's status.

Example request:

```json
{
  "status": "Acknowledged"
}
```

Allowed values:

- `Active`
- `Acknowledged`
- `Resolved`

Successful response: updated alert object.

Possible errors:
- `404`: Alert not found.
- `422`: Invalid status.

### Current demonstration alert rules

The backend creates an indicator alert when its ML score is at least 50.

| Indicator score | Severity |
|---|---|
| Below 50 | No alert |
| 50Ã¢â‚¬â€œ74.99 | Medium |
| 75 or above | High |

These are application-level demonstration rules, not medical or NASA safety thresholds.

## 7. Simulation API

### POST `/api/v1/simulation/run`

Runs a hypothetical scenario using the same ML risk engine without saving hypothetical telemetry.

Example request:

```json
{
  "astronaut_id": "AST-001",
  "metrics": {
    "radiation_dose_rate_usv_per_hour": 3.0
  }
}
```

Supported metric keys:

- `heart_rate_bpm`
- `spo2_percent`
- `sleep_hours_last_24h`
- `body_temperature_celsius`
- `radiation_dose_rate_usv_per_hour`
- `activity_level_percent`
- `fatigue_level_0_10`

The endpoint returns:

- `astronaut_id`
- `baseline`: baseline ML risk result
- `simulation`: hypothetical ML risk result
- `changed_factors`: original and simulated values for submitted metrics

Possible errors:
- `404`: Astronaut not found.
- `422`: Empty metrics, unsupported metric, invalid metric or unavailable baseline data.
- `503`: ML module unavailable.

**Important:** Simulation is non-persistent. Hypothetical readings are not inserted into telemetry history.

## 8. Chat API

### POST `/api/v1/chat`

Saves a user message and provides a stable handoff contract for future AI integration.

Example request:

```json
{
  "astronaut_id": "AST-001",
  "message": "Explain the astronaut's current radiation risk."
}
```

Optional fields:

- `astronaut_id`
