from typing import cast
import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.utils import AuthorizationData

client = TestClient(app)

def get_user_profile(
    authorization: AuthorizationData,
    username: str | None = None
) -> dict[str, str]:
    endpoint = f"users/{username}" if username else "users/me"
    response = client.get(endpoint, headers=authorization.header)
    return cast(dict[str, str], response.json())

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
    user_profile = get_user_profile(authorization)
    assert user_profile == {
        "username": authorization.credentials["username"],
        "bio": None,
        "totalPosts": 0
    }

@pytest.mark.parametrize(
    "update_fields",
    [
        {"bio": "I'm a Backend Python Developer!"},
        {"bio": "And I love Japan!"},
        {"bio": "I'm sure I'll get there in the future!"}
    ]
)
def test_updating_current_user_profile(
    authorization: AuthorizationData,
    update_fields: dict[str, str]
) -> None:
    user_profile_before_update = get_user_profile(authorization)
    expected_user_profile_after_update = (
        user_profile_before_update | update_fields
    )
    response = client.put("/users/me", headers=authorization.header, json=update_fields)
    assert response.status_code == 200
    assert response.json() == expected_user_profile_after_update
    user_profile_after_update = get_user_profile(authorization)
    assert user_profile_after_update == expected_user_profile_after_update