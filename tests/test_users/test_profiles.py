import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.utils import AuthorizationData

client = TestClient(app)

@pytest.mark.parametrize(
    "authorization",
    [
        {"username": "john_doe", "password": "SuperSecret"},
        {"username": "JaneDoe", "password": "LoremIpsum"},
        {"username": "mysterious_hacker", "password": "LiterallyUnhackablePassword"}
    ],
    indirect=True
)
def test_retrieving_current_user_profile(authorization: AuthorizationData) -> None:
    response = client.get("/users/me", headers=authorization.header)
    user_profile = response.json()
    assert user_profile == {
        "username": authorization.credentials["username"],
        "bio": None,
        "totalPosts": 0
    }