from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test the GET root endpoint


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

# Test the GET greet endpoint


def test_greet_name():
    response = client.get("/greet/Alice")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Alice!"}

# Test the POST greet endpoint with valid data


def test_create_greeting_valid():
    response = client.post(
        "/greet",
        json={"name": "Bob", "age": 30}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Bob! You are 30 years old."}

# Test the POST greet endpoint with invalid age (negative)


def test_create_greeting_negative_age():
    response = client.post(
        "/greet",
        json={"name": "Charlie", "age": -5}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Age cannot be negative"}

# Test the POST greet endpoint with missing data


def test_create_greeting_missing_field():
    response = client.post(
        "/greet",
        json={"name": "David"}  # Missing 'age'
    )
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()
    assert any("age" in error["loc"] for error in response.json()["detail"])
