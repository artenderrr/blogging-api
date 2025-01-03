import pytest
import bcrypt
from tinydb import TinyDB, where
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def assert_credentials_creation(credentials: dict[str, str]) -> None:
    db = TinyDB("app/db/credentials.json")
    assert db.contains(where("username") == credentials["username"])
    assert bcrypt.checkpw(
        credentials["password"].encode("utf-8"),
        db.get(where("username") == credentials["username"])["password"].encode("utf-8")
    )

def assert_user_creation(credentials: dict[str, str]) -> None:
    db = TinyDB("app/db/users.json")
    assert db.contains(where("username") == credentials["username"])
    created_user = db.get(where("username") == credentials["username"])
    assert created_user["bio"] is None
    assert created_user["totalPosts"] == 0

@pytest.mark.parametrize(
    "credentials",
    [
        {"username": "john_doe", "password": "SuperSecret"},
        {"username": "JaneDoe", "password": "LoremIpsum"},
        {"username": "mysterious_hacker", "password": "LiterallyUnhackablePassword"}
    ]
)
def test_on_valid_credentials(credentials: dict[str, str]) -> None:
    response = client.post("/register", json=credentials)
    assert response.status_code == 201
    assert_credentials_creation(credentials)
    assert_user_creation(credentials)

@pytest.mark.parametrize(
    "credentials",
    [
        {"username": "john_doe", "password": "RandomPassword"}
    ]
)
def test_with_taken_username(credentials: dict[str, str]) -> None:
    db = TinyDB("app/db/credentials.json")
    db.insert(credentials)
    response = client.post("/register", json=credentials)
    assert response.status_code == 409

@pytest.mark.parametrize(
    "credentials",
    [
        {"username": "usr", "password": "SomePassword"},
        {"username": "valid_username", "password": "short"},
        {"username": "valid_username", "password": "no_upper_case"},
    ]
)
def test_on_invalid_credentials(credentials: dict[str, str]) -> None:
    response = client.post("/register", json=credentials)
    assert response.status_code == 422