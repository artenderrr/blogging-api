import pytest
from tinydb import TinyDB, where
from fastapi.testclient import TestClient
from app.main import app
from tests.utils import AuthorizationData
from tests.test_posts.utils import test_posts

client = TestClient(app)

@pytest.mark.parametrize("post", test_posts)
def test_post_creation(
    authorization: AuthorizationData,
    post: dict[str, str]
) -> None:
    db = TinyDB("app/db/posts.json")
    response = client.post(
        "/posts",
        headers=authorization.header,
        json=post
    )
    assert response.status_code == 201
    created_post_id = response.json()["postId"]
    created_post = db.get(where("postId") == created_post_id)
    for key in post:
        assert key in created_post and created_post[key] == post[key]
    for key in ("author", "timestamp", "postId"):
        assert key in created_post