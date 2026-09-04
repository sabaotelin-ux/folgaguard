from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)
API_KEY = "aegis_secret_token_2026"

def test_metrics_success():
    response = client.get("/metrics", headers={"X-API-Key": API_KEY})
    assert response.status_code == 200
    assert response.json() == {"total_decisions": 431, "status": "active"}

def test_metrics_unauthorized():
    response = client.get("/metrics", headers={"X-API-Key": "wrong_token"})
    assert response.status_code == 403

def test_decide_success():
    payload = {
        "task_id": "T-200",
        "action": "route_remote",
        "priority": 1,
        "company_size": 20,
        "latency_ms": 30.0,
        "error_rate": 0.005
    }
    response = client.post("/decide", json=payload, headers={"X-API-Key": API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["task_id"] == "T-200"

print("Arquivo de testes test_api.py criado com sucesso!")
