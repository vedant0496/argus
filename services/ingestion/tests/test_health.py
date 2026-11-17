from fastapi.testclient import TestClient

from argus_ingestion.app import create_app


def test_healthz() -> None:
    response = TestClient(create_app()).get("/healthz")
    assert response.status_code == 200
    assert response.json()["service"] == "ingestion"
