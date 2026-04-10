from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_update_ticket(client):
    create_response = client.post("/tickets/", json={
        "title": "Ticket para da update",
        "description": "Descricao do ticket",
        "priority": "medium"
    })

    assert create_response.status_code == 201

    create_data = create_response.json()
    data_id = create_data["id"]

    update_ticket = client.patch(f"/tickets/{data_id}", json={
        "title": "Ticket para da update: Upado",
        "description": "Descricao do ticket: Upado",
        "priority": "low",
        "status": "done"
    })

    assert update_ticket.status_code == 200

    update_ticket_json = update_ticket.json()

    assert update_ticket_json["id"] == data_id
    assert update_ticket_json["title"] == "Ticket para da update: Upado"
    assert update_ticket_json["description"] == "Descricao do ticket: Upado"
    assert update_ticket_json["priority"] == "low"
    assert update_ticket_json["status"] == "done"

def test_update_ticket_not_found(client):
    response = client.patch("/tickets/9999", json={
        "title": "Nao existe"
    })

    assert response.status_code == 404
