from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# def test_root_not_found():
#     response = client.get("/")
#     assert response.status_code == 404

# def test_create_ticket(client):
#     payloand = {

#         "title":"Teste de titulo",
#         "description":"Teste de descricao",
#         "priority":"medium"

#     }

#     response = client.post("/tickets/",json=payloand)

#     assert response.status_code == 201

#     data = response.json()
#     assert data["title"] == "Teste de titulo"
#     assert data["description"] == "Teste de descricao"
#     assert data["priority"] == "medium"
#     assert data["status"] == "open"
#     assert "id" in data

# def test_create_ticket_without_title_returns_422(client):
#     payload = {
#         "description": "Teste sem titulo",
#         "priority": "medium"
#     }

#     response = client.post("/tickets/", json=payload)

#     assert response.status_code == 422


# def test_list_tickets_returns_created_tickets(client):
#     client.post("/tickets/", json={
#         "title": "Ticket 1",
#         "description": "Descricao 1",
#         "priority": "low"
#     })

#     client.post("/tickets/", json={
#         "title": "Ticket 2",
#         "description": "Descricao 2",
#         "priority": "medium"
#     })


#     response = client.get("/tickets/")

#     assert response.status_code == 200

#     data = response.json()

#     assert "items" in data
#     assert len(data["items"]) == 2

# def test_get_ticket_by_id(client):
#     response = client.post("/tickets/", json={
#          "title": "Ticket 1",
#          "description": "Descricao 1",
#          "priority": "low"
#      })
    

#     data = response.json()
#     id_ticket = data["id"]

#     get_response_of_id = client.get(f"/tickets/{id_ticket}")

#     assert get_response_of_id.status_code == 200


# def test_get_ticket_by_id_not_found(client):
    
#     id = 9999
#     response = client.get(f"/tickets/{id}")

#     assert response.status_code == 404


# def test_get_ticket_by_title(client):
#     create_response = client.post("/tickets/", json={
#         "title": "Titulo Unico",
#         "description": "Descricao teste",
#         "priority": "medium"
#     })

#     assert create_response.status_code == 201

#     response = client.get("/tickets/by-title/Titulo Unico")

#     assert response.status_code == 200

#     data = response.json()
#     assert data["title"] == "Titulo Unico"
#     assert data["description"] == "Descricao teste"
#     assert data["priority"] == "medium"

# def test_get_ticket_by_title_not_found(client):
#     response = client.get("/tickets/by-title/Titulo Inexistente")
#     assert response.status_code == 404


# def test_delete_ticket(client):
#     create_response = client.post("/tickets/", json={
#         "title": "Ticket para deletar",
#         "description": "Descricao do ticket",
#         "priority": "medium"
#     })

#     created_data = create_response.json()
#     ticket_id = created_data["id"]

#     delete_response = client.delete(f"/tickets/{ticket_id}")
#     assert delete_response.status_code == 204

#     get_response = client.get(f"/tickets/{ticket_id}")
#     assert get_response.status_code == 404

# def test_update_ticket(client):
#     create_response = client.post("/tickets/", json={
#         "title": "Ticket para da update",
#         "description": "Descricao do ticket",
#         "priority": "medium"
#     })

#     assert create_response.status_code == 201

#     create_data = create_response.json()
#     data_id = create_data["id"]

#     update_ticket = client.patch(f"/tickets/{data_id}", json={
#         "title": "Ticket para da update: Upado",
#         "description": "Descricao do ticket: Upado",
#         "priority": "low",
#         "status": "done"
#     })

#     assert update_ticket.status_code == 200

#     update_ticket_json = update_ticket.json()

#     assert update_ticket_json["id"] == data_id
#     assert update_ticket_json["title"] == "Ticket para da update: Upado"
#     assert update_ticket_json["description"] == "Descricao do ticket: Upado"
#     assert update_ticket_json["priority"] == "low"
#     assert update_ticket_json["status"] == "done"

# def test_update_ticket_not_found(client):
#     response = client.patch("/tickets/9999", json={
#         "title": "Nao existe"
#     })

#     assert response.status_code == 404


def test_list_tickets_with_pagination(client):
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

    response = client.get("/tickets/?page=1&page_size=1")

    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["page"] == 1
    assert data["page_size"] == 1
    assert data["total"] == 2
    assert data["pages"] == 2

def test_list_tickets_with_pagination(client):
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

    response = client.get("/tickets/?page=1&page_size=1")

    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["page"] == 1
    assert data["page_size"] == 1
    assert data["total"] == 2
    assert data["pages"] == 2

def test_list_tickets_filter_by_priority(client):
    client.post("/tickets/", json={
        "title": "Ticket low",
        "description": "Descricao low",
        "priority": "low"
    })

    client.post("/tickets/", json={
        "title": "Ticket medium",
        "description": "Descricao medium",
        "priority": "medium"
    })

    response = client.get("/tickets/?priority=low")

    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Ticket low"
    assert data["items"][0]["priority"] == "low"

def test_list_tickets_filter_by_status(client):
    client.post("/tickets/", json={
        "title": "Ticket aberto",
        "description": "Descricao aberto",
        "priority": "low"
    })

    created_response = client.post("/tickets/", json={
        "title": "Ticket fechado",
        "description": "Descricao fechado",
        "priority": "medium"
    })

    created_data = created_response.json()
    ticket_id = created_data["id"]

    patch_response = client.patch(f"/tickets/{ticket_id}", json={
        "status": "closed"
    })
    assert patch_response.status_code == 200

    response = client.get("/tickets/?status=closed")

    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Ticket fechado"
    assert data["items"][0]["status"] == "closed"

def test_list_tickets_sort_by_priority_asc(client):
    client.post("/tickets/", json={
        "title": "Ticket medium",
        "description": "Descricao medium",
        "priority": "medium"
    })

    client.post("/tickets/", json={
        "title": "Ticket low",
        "description": "Descricao low",
        "priority": "low"
    })

    response = client.get("/tickets/?sort=priority&order=asc")

    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 2

def test_list_tickets_invalid_page_returns_422(client):
    response = client.get("/tickets/?page=0")

    assert response.status_code == 422

def test_list_tickets_invalid_page_size_returns_422(client):
    response = client.get("/tickets/?page_size=101")

    assert response.status_code == 422

def test_list_tickets_invalid_date_range_returns_400(client):
    response = client.get(
        "/tickets/?created_from=2026-01-02T10:00:00&created_to=2026-01-01T10:00:00"
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "created_from cannot be after created_to"

def test_delete_ticket_not_found(client):
    response = client.delete("/tickets/9999")

    assert response.status_code == 404