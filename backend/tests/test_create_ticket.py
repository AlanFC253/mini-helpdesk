from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_not_found():
    response = client.get("/")
    assert response.status_code == 404

def test_create_ticket(client):
    payloand = {

        "title":"Teste de titulo",
        "description":"Teste de descricao",
        "priority":"medium"

    }

    response = client.post("/tickets/",json=payloand)

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Teste de titulo"
    assert data["description"] == "Teste de descricao"
    assert data["priority"] == "medium"
    assert data["status"] == "open"
    assert "id" in data

def test_create_ticket_without_title_returns_422(client):
    payload = {
        "description": "Teste sem titulo",
        "priority": "medium"
    }

    response = client.post("/tickets/", json=payload)

    assert response.status_code == 422
