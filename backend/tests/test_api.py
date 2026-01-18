import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_register():
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "nickname": "Test User",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data


def test_login_success():
    response = client.post(
        "/auth/login", json={"email": "test@example.com", "password": "password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_failure():
    response = client.post(
        "/auth/login", json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_get_trips_unauthorized():
    response = client.get("/trips")
    assert response.status_code == 403


def test_create_trip_unauthorized():
    trip_data = {
        "title": "Test Trip",
        "destinations": ["北京"],
        "start_date": "2024-03-01",
        "end_date": "2024-03-05",
        "budget": {
            "total": 5000,
            "transport": 1500,
            "accommodation": 1750,
            "food": 1000,
            "activities": 750,
        },
    }
    response = client.post("/trips", json=trip_data)
    assert response.status_code == 403
