def test_health(client):
    r=client.get("/health"); assert r.status_code==200 and r.json()["status"]=="ok"
def test_astronauts(client):
    r=client.get("/api/v1/astronauts"); assert r.status_code==200 and len(r.json())>=4
def test_unknown_astronaut(client):
    assert client.get("/api/v1/astronauts/UNKNOWN").status_code==404
def test_telemetry_create_and_history(client):
    payload={"astronaut_id":"AST-001","heart_rate_bpm":73,"spo2_percent":98,"sleep_hours_last_24h":7,"radiation_dose_rate_usv_per_hour":0.4,"fatigue_level_0_10":2}
    r=client.post("/api/v1/telemetry",json=payload); assert r.status_code==201
    assert client.get("/api/v1/astronauts/AST-001/telemetry").status_code==200
def test_invalid_metric(client):
    payload={"astronaut_id":"AST-001","spo2_percent":150}
    assert client.post("/api/v1/telemetry",json=payload).status_code==422
def test_alert_update_unknown(client):
    assert client.patch("/api/v1/alerts/999",json={"status":"Resolved"}).status_code==404
def test_simulation_unknown(client):
    assert client.post("/api/v1/simulation/run",json={"astronaut_id":"UNKNOWN","metrics":{"heart_rate_bpm":80}}).status_code==404
def test_chat_pending_contract(client):
    r=client.post("/api/v1/chat",json={"message":"Summarize my status"})
    assert r.status_code==200 and r.json()["status"]=="integration_pending"


def test_risk_analysis_persists_assessment(client, monkeypatch):
    import app.services.risk_service as service
    fake = {"score": 12.5, "category": "low", "status": "available", "indicators": {}, "warnings": []}
    monkeypatch.setattr(service, "analyze", lambda current, history: fake)
    response = client.post("/api/v1/astronauts/AST-001/risk/analyze")
    assert response.status_code == 200
    assert response.json()["score"] == 12.5
    history = client.get("/api/v1/astronauts/AST-001/risk")
    assert history.status_code == 200 and len(history.json()) == 1

def test_simulation_does_not_create_telemetry(client, monkeypatch):
    import app.api.routes.simulation as route
    fake = {"score": 10.0, "category": "low", "status": "available", "indicators": {}}
    monkeypatch.setattr(route, "analyze_simulation", lambda astronaut_id, metrics, history: fake)
    before = len(client.get("/api/v1/astronauts/AST-001/telemetry").json())
    response = client.post("/api/v1/simulation/run", json={"astronaut_id": "AST-001", "metrics": {"heart_rate_bpm": 90}})
    after = len(client.get("/api/v1/astronauts/AST-001/telemetry").json())
    assert response.status_code == 200
    assert response.json()["simulation"]["score"] == 10.0
    assert before == after
