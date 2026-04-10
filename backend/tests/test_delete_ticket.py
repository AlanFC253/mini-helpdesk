from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_delete_ticket(client):
    create_response = client.post("/tickets/", json={
        "title": "Ticket para deletar",
        "description": "Descricao do ticket",
        "priority": "medium"
    })

    created_data = create_response.json()
    ticket_id = created_data["id"]

    delete_response = client.delete(f"/tickets/{ticket_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tickets/{ticket_id}")
    assert get_response.status_code == 404

def test_delete_ticket_not_found(client):
    response = client.delete("/tickets/9999")

    assert response.status_code == 404