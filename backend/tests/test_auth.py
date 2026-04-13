from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_success(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "123456"
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "senhaerrada"
        },
    )

    assert response.status_code == 401

def test_create_ticket_without_token_returns_401(client):
    response = client.post("/tickets/", json={
        "title": "Ticket protegido",
        "description": "Sem token",
        "priority": "medium"
    })

    assert response.status_code == 401