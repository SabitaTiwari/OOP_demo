import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def product_payload():
    return {
        "name": "Mouse",
        "description": "Wireless mouse for developers",
        "price": 25.5,
        "stock": 10,
    }


@pytest.fixture
def created_product(client, product_payload):
    response = client.post("/api/v1/products", json=product_payload)

    assert response.status_code == 201

    return response.json()


def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "OOP FastAPI Demo is running"


def test_create_product(client, product_payload):
    response = client.post("/api/v1/products", json=product_payload)

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["name"] == product_payload["name"]
    assert data["description"] == product_payload["description"]
    assert data["price"] == product_payload["price"]
    assert data["stock"] == product_payload["stock"]


def test_list_products(client):
    response = client.get("/api/v1/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_product_by_id(client, created_product):
    product_id = created_product["id"]

    response = client.get(f"/api/v1/products/{product_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == created_product["name"]
    assert data["price"] == created_product["price"]
    assert data["stock"] == created_product["stock"]


def test_update_product(client, created_product):
    product_id = created_product["id"]

    update_payload = {
        "name": "Updated Mouse",
        "price": 30.0,
    }

    response = client.put(
        f"/api/v1/products/{product_id}",
        json=update_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Updated Mouse"
    assert data["price"] == 30.0

    # Stock was not updated, so it should remain same as before.
    assert data["stock"] == created_product["stock"]


def test_delete_product(client, created_product):
    product_id = created_product["id"]

    delete_response = client.delete(f"/api/v1/products/{product_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Product deleted successfully"

    get_response = client.get(f"/api/v1/products/{product_id}")

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Product not found"


def test_purchase_product(client, created_product):
    product_id = created_product["id"]

    purchase_response = client.post(
        f"/api/v1/products/{product_id}/purchase",
        json={"quantity": 3},
    )

    assert purchase_response.status_code == 200

    data = purchase_response.json()

    assert data["id"] == product_id
    assert data["stock"] == created_product["stock"] - 3


def test_purchase_more_than_available_stock(client, created_product):
    product_id = created_product["id"]

    response = client.post(
        f"/api/v1/products/{product_id}/purchase",
        json={"quantity": 100},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough stock available"


def test_apply_discount(client, created_product):
    product_id = created_product["id"]

    response = client.post(
        f"/api/v1/products/{product_id}/discount",
        json={"percentage": 10},
    )

    assert response.status_code == 200

    data = response.json()

    expected_price = created_product["price"] - (created_product["price"] * 0.10)

    assert data["id"] == product_id
    assert data["price"] == expected_price


def test_apply_invalid_discount(client, created_product):
    product_id = created_product["id"]

    response = client.post(
        f"/api/v1/products/{product_id}/discount",
        json={"percentage": 100},
    )

    assert response.status_code == 422


def test_product_not_found(client):
    response = client.get("/api/v1/products/unknown-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_create_product_with_negative_price(client):
    payload = {
        "name": "Invalid Product",
        "description": "Product with invalid price",
        "price": -10.0,
        "stock": 5,
    }

    response = client.post("/api/v1/products", json=payload)

    assert response.status_code == 422


def test_create_product_with_missing_name(client):
    payload = {
        "description": "Product without name",
        "price": 20.0,
        "stock": 5,
    }

    response = client.post("/api/v1/products", json=payload)

    assert response.status_code == 422


def test_create_product_with_negative_stock(client):
    payload = {
        "name": "Invalid Stock Product",
        "description": "Product with invalid stock",
        "price": 20.0,
        "stock": -5,
    }

    response = client.post("/api/v1/products", json=payload)

    assert response.status_code == 422