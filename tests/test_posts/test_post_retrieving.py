import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.utils import AuthorizationData
from tests.test_posts.utils import test_posts

client = TestClient(app)

class TestRetrievingPostByID:
    @pytest.mark.parametrize("post", test_posts)
    def test_retrieving_existing_post(
        self,
        authorization: AuthorizationData,
        post: dict[str, str]
    ) -> None:
        client.post("/posts", headers=authorization.header, json=post)
        response = client.get("/posts/1", headers=authorization.header)
        assert response.status_code == 200
        retrieved_post = response.json()
        for key in post:
            assert key in retrieved_post and retrieved_post[key] == post[key]
        for key in ("author", "timestamp", "postId"):
            assert key in retrieved_post

    def test_retrieving_nonexistent_post(
        self,
        authorization: AuthorizationData
    ) -> None:
        response = client.get("/posts/1", headers=authorization.header)
        assert response.status_code == 404
        assert response.json() == {"detail": "Post with provided ID doesn't exist"}