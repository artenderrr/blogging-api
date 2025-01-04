import pytest
from tinydb import TinyDB, where
from fastapi.testclient import TestClient
from app.main import app
from tests.utils import AuthorizationData

client = TestClient(app)

@pytest.mark.parametrize(
    "post",
    [
        {
            "title": "Exploring the Stars",
            "content": "The vast universe holds mysteries that humanity has only begun to uncover. From black holes to distant galaxies, each discovery fuels our curiosity."
        },
        {
            "title": "The Art of Minimalism",
            "content": "Living with less can lead to more clarity and joy. Minimalism teaches us to prioritize what truly matters in life."
        },
        {
            "title": "A Journey Through the Rainforest",
            "content": "Rainforests are home to countless species of plants and animals, many of which remain undiscovered. They are vital to the health of our planet."
        }
    ]
)
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