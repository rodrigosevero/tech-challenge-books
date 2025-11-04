from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "dataset_size" in data
