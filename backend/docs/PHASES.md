# COSMOCare Backend — phased implementation

## Phase 1 — Foundation
FastAPI application, environment settings, CORS, `/health`, versioned router, SQLAlchemy engine/session, table initialization.

## Phase 2 — Data layer
Astronaut, telemetry, risk assessment, alert, conversation and message models. SQLite seed data (4 illustrative astronauts and 30 hourly samples each). No credentials are stored in the database.

## Phase 3 — API contracts
Pydantic request/response schemas and endpoints for astronauts, telemetry, risk history, alerts, alert status, simulation and chat handoff. OpenAPI docs at `/docs`.

## Phase 4 — ML integration
`app/services/ml_service.py` loads the separate ML repository from `ML_SRC_PATH` and calls its `calculate_baseline` and `calculate_risk` functions. Keep the ML developer's `ml/` directory untouched. Configure the path to the extracted ML repo's `ml/src` directory.

Risk results are experimental software indicators only, not medical diagnosis or safety determinations. Alert rules are application-level demonstration rules (indicator score >= 50).

## Phase 5 — Simulation and AI handoff
Simulation runs the same ML engine against hypothetical metrics without inserting a telemetry row. `/chat` stores user messages and returns `integration_pending`; the AI developer must implement provider invocation and assistant message persistence before claiming AI integration complete.

## Phase 6 — Tests and integration
Run `pytest`. Commit this folder on branch `backend` and open a PR targeting `integration`. Coordinate final payload names with frontend/ML/AI owners before merging.
