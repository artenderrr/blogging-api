import pytest
import bcrypt
from tinydb import TinyDB
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.parametrize(
    "credentials",
    [
        {"username": "john_doe", "password": "SuperSecret"},
        {"username": "JaneDoe", "password": "LoremIpsum"},
        {"username": "mysterious_hacker", "password": "LiterallyUnhackablePassword"}
    ]
)
def test_on_valid_credentials(credentials: dict[str, str]) -> None:
    db = TinyDB("app/db/credentials.json")
    db.insert(
        {
            "username": credentials["username"],
            "password": bcrypt.hashpw(
                credentials["password"].encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")
        }
    )
    response = client.post("/login", json=credentials)
    assert response.status_code == 200

@pytest.mark.parametrize(
    "credentials",
    [
        {"username": "non_existent", "password": "missing"}
    ]
)
def test_on_nonexistent_user(credentials: dict[str, str]) -> None:
    response = client.post("/login", json=credentials)
    assert response.status_code == 401

@pytest.mark.parametrize(
    "credentials",
    [
        {"username": "john_doe", "password": "something_invalid"}
    ]
)
def test_on_invalid_password(credentials: dict[str, str]) -> None:
    db = TinyDB("app/db/credentials.json")
    db.insert(
        {
            "username": credentials["username"],
            "password": bcrypt.hashpw(b"SecurePassword", bcrypt.gensalt()).decode("utf-8")
        }
    )
    response = client.post("/login", json=credentials)
    assert response.status_code == 401