from typing import cast
from tinydb import TinyDB, where
from fastapi.testclient import TestClient
from app.main import app
from tests.utils import AuthorizationData
from tests.test_posts.utils import create_test_post # noqa

client = TestClient(app)

def get_total_posts(authorization: AuthorizationData) -> int:
    response = client.get("/users/me", headers=authorization.header)
    total_posts = cast(int, response.json()["totalPosts"])
    return total_posts

def test_for_valid_response_code(
    authorization: AuthorizationData
) -> None:
    response = client.delete("/posts/1", headers=authorization.header)
    assert response.status_code == 204

def test_for_post_absence_after_deleting(
    authorization: AuthorizationData
) -> None:
    db = TinyDB("app/db/posts.json")
    assert db.contains(where("postId") == 1)
    client.delete("/posts/1", headers=authorization.header)
    assert not db.contains(where("postId") == 1)

def test_for_valid_total_posts_after_deleting(
    authorization: AuthorizationData
) -> None:
    total_posts_before_deleting = get_total_posts(authorization)
    client.delete("/posts/1", headers=authorization.header)
    total_posts_after_deleting = get_total_posts(authorization)
    assert total_posts_after_deleting == total_posts_before_deleting - 1

def test_for_restricted_access() -> None:
    authorization = AuthorizationData(
        credentials={"username": "someone_else", "password": "SomePasswordHere"}
    )
    response = client.delete("/posts/1", headers=authorization.header)
    assert response.status_code == 403
    assert response.json() == {"detail": "Post's ownership doesn't match the current user"}