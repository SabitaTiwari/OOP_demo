from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "OOP FastAPI Demo is running"


def test_create_product():
    payload = {
        "name": "Mouse",
        "description": "Wireless mouse for developers",
        "price": 25.5,
        "stock": 10,
    }

    response = client.post("/api/v1/products", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["stock"] == payload["stock"]


def test_list_products():
    response = client.get("/api/v1/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_purchase_product():
    create_payload = {
        "name": "Monitor",
        "description": "External monitor",
        "price": 300.0,
        "stock": 8,
    }

    create_response = client.post("/api/v1/products", json=create_payload)
    product_id = create_response.json()["id"]

    purchase_response = client.post(
        f"/api/v1/products/{product_id}/purchase",
        json={"quantity": 3},
    )

    assert purchase_response.status_code == 200
    assert purchase_response.json()["stock"] == 5


def test_product_not_found():
    response = client.get("/api/v1/products/unknown-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"