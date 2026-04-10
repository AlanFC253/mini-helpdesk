from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)



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
        "status": "done"
    })
    assert patch_response.status_code == 200

    response = client.get("/tickets/?status=done")
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Ticket fechado"
    assert data["items"][0]["status"] == "done"

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

