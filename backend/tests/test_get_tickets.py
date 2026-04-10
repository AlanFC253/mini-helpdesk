from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

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


def test_get_ticket_by_title(client):
    create_response = client.post("/tickets/", json={
        "title": "Titulo Unico",
        "description": "Descricao teste",
        "priority": "medium"
    })

    assert create_response.status_code == 201

    response = client.get("/tickets/by-title/Titulo Unico")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Titulo Unico"
    assert data[0]["description"] == "Descricao teste"
    assert data[0]["priority"] == "medium"

def test_get_ticket_by_title_not_found(client):
    response = client.get("/tickets/by-title/Titulo Inexistente")
    assert response.status_code == 404
