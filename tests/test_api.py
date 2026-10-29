from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_lists_sample_routes() -> None:
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["docs"] == "/docs"
    assert body["items"] == "/api/v1/items"
    assert body["users"] == "/api/v1/users"


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_items_returns_seed_data() -> None:
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert [item["name"] for item in body["results"]] == ["Notebook", "Coffee mug"]


def test_filter_items_by_tag_and_name() -> None:
    by_tag = client.get("/api/v1/items", params={"tag": "kitchen"})
    assert [item["name"] for item in by_tag.json()["results"]] == ["Coffee mug"]

    by_name = client.get("/api/v1/items", params={"q": "note"})
    assert [item["name"] for item in by_name.json()["results"]] == ["Notebook"]


def test_create_get_update_and_delete_item() -> None:
    created = client.post(
        "/api/v1/items",
        json={"name": "Pen", "description": "Black ink", "price": 2.5, "tags": ["stationery"]},
    )
    assert created.status_code == 201
    item_id = created.json()["id"]

    fetched = client.get(f"/api/v1/items/{item_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Pen"

    updated = client.patch(f"/api/v1/items/{item_id}", json={"price": 3})
    assert updated.status_code == 200
    assert updated.json()["price"] == 3
    assert updated.json()["name"] == "Pen"

    deleted = client.delete(f"/api/v1/items/{item_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/items/{item_id}").status_code == 404


def test_rejects_invalid_item() -> None:
    response = client.post("/api/v1/items", json={"name": "", "price": 0})
    assert response.status_code == 422


def test_missing_item_is_404() -> None:
    assert client.get("/api/v1/items/999").status_code == 404
    assert client.delete("/api/v1/items/999").status_code == 404


def test_users_flow() -> None:
    listing = client.get("/api/v1/users", params={"role": "admin"})
    assert listing.status_code == 200
    assert [user["email"] for user in listing.json()["results"]] == ["ada@example.com"]

    created = client.post(
        "/api/v1/users",
        json={"name": "Grace Hopper", "email": "Grace@Example.com", "role": "member"},
    )
    assert created.status_code == 201
    assert created.json()["email"] == "grace@example.com"

    duplicate = client.post(
        "/api/v1/users",
        json={"name": "Grace Again", "email": "grace@example.com"},
    )
    assert duplicate.status_code == 409

    fetched = client.get(f"/api/v1/users/{created.json()['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Grace Hopper"
    assert client.get("/api/v1/users/999").status_code == 404
