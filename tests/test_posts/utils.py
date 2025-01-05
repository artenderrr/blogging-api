import pytest
from tests.utils import AuthorizationData
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

test_posts = [
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

test_post_update_fields = [
    {"title": "Edited post title"},
    {"content": "Edited post content"},
    {"title": "Another title", "content": "Another content"}
]

@pytest.fixture(autouse=True)
def create_test_post(
    authorization: AuthorizationData
) -> None:
    client.post("/posts", headers=authorization.header, json=test_posts[1])