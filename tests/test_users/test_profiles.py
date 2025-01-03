from typing import cast
import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.utils import AuthorizationData
from tests.test_users.utils import test_credentials

client = TestClient(app)

def get_user_profile(
    authorization: AuthorizationData,
    username: str | None = None
) -> dict[str, str]:
    endpoint = f"users/{username}" if username else "users/me"
    response = client.get(endpoint, headers=authorization.header)
    return cast(dict[str, str], response.json())

@pytest.mark.parametrize("authorization", test_credentials, indirect=True)
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
    assert response.json() == expected_user_profile_after_update
    user_profile_after_update = get_user_profile(authorization)
    assert user_profile_after_update == expected_user_profile_after_update

@pytest.mark.parametrize("register_credentials", test_credentials)
def test_retrieving_specific_user_profile_by_username(
    authorization: AuthorizationData,
    register_credentials: dict[str, str]
) -> None:
    client.post("/register", json=register_credentials)
    user_profile = get_user_profile(authorization, register_credentials["username"])
    assert user_profile == {
        "username": register_credentials["username"],
        "bio": None,
        "totalPosts": 0
    }