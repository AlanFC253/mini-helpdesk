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


def test_list_tickets_returns_created_tickets(client):
    client.post("/tickets/", json={
        "title": "Ticket 1",
        "description": "Descricao 1",
        "priority": "low"
    })

    client.post("/tickets/", json={
        "title": "Ticket 2",
        "description": "Descricao 2",
        "priority": "medium"
    })


    response = client.get("/tickets/")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert len(data["items"]) == 2

def test_get_ticket_by_id(client):
    response = client.post("/tickets/", json={
         "title": "Ticket 1",
         "description": "Descricao 1",
         "priority": "low"
     })
    

    data = response.json()
    id_ticket = data["id"]

    get_response_of_id = client.get(f"/tickets/{id_ticket}")

    assert get_response_of_id.status_code == 200


def test_get_ticket_by_id_not_found(client):
    
    id = 9999
    response = client.get(f"/tickets/{id}")

    assert response.status_code == 404



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