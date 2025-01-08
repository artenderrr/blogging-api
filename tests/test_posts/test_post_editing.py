import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.utils import AuthorizationData
from tests.test_posts.utils import create_test_post # noqa
from tests.test_posts.utils import test_post_update_fields

client = TestClient(app)

def test_for_valid_response_code(
    authorization: AuthorizationData
) -> None:
    response = client.put(
        "/posts/1",
        headers=authorization.header,
        json=test_post_update_fields[1]
    )
    assert response.status_code == 200

@pytest.mark.parametrize("update_fields", test_post_update_fields)
def test_for_valid_response_body(
    authorization: AuthorizationData,
    update_fields: dict[str, str]
) -> None:
    post_before_editing = client.get(
        "/posts/1",
        headers=authorization.header
    ).json()
    response = client.put(
        "/posts/1",
        headers=authorization.header,
        json=update_fields
    )
    assert response.json() == (
        post_before_editing | update_fields
    )

def test_for_restricted_access() -> None:
    authorization = AuthorizationData(
        credentials={"username": "someone_else", "password": "SomePasswordHere"}
    )
    response = client.put(
        "/posts/1",
        headers=authorization.header,
        json=test_post_update_fields[1]
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Post's ownership doesn't match the current user"}