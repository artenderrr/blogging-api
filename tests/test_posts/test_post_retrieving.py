from typing import cast
from datetime import datetime
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

class TestRetrievingMultiplePosts:
    def create_test_posts(
        self,
        posts: list[dict[str, str]],
        authorization: AuthorizationData
    ) -> None:
        for post in posts:
            client.post(
                "/posts",
                headers=authorization.header,
                json=post
            )

    def test_for_correct_order(
        self,
        authorization: AuthorizationData
    ) -> None:
        self.create_test_posts(test_posts, authorization)
        response = client.get("/posts", headers=authorization.header)
        retrieved_posts = response.json()
        assert type(retrieved_posts) is list
        assert retrieved_posts == [*reversed(test_posts)]

    def test_for_correct_author(
        self,
        authorization: AuthorizationData
    ) -> None:
        test_users = ["violet_roses", "nutcracker", "kinshu"]
        for n, test_user in enumerate(test_users):
            self.create_test_posts(
                test_posts[n * 3 : (n + 1) * 3],
                AuthorizationData(
                    credentials={
                        "username": test_user,
                        "password": f"{test_user.title()}Password"
                    }
                )
            )
        request_user = test_user[1]
        response = client.get(
            f"/posts?author={request_user}",
            headers=authorization.header
        )
        retrieved_posts = response.json()
        assert type(retrieved_posts) is list
        assert all(post["author"] == request_user for post in retrieved_posts)
        assert len(retrieved_posts) == 3

    @pytest.mark.parametrize(
        "amount_to_create, amount_to_retrieve",
        [
            (3, "default"), (6, "default"),
            (0, 1), (2, 1),
            (1, 3), (4, 3),
            (3, 5), (6, 5),
            (5, 10), (15, 10),
        ]
    )
    def test_for_correct_amount_without_specifying_author(
        self,
        authorization: AuthorizationData,
        amount_to_create: int,
        amount_to_retrieve: str | int
    ) -> None:
        self.create_test_posts(test_posts[:amount_to_create], authorization)
        if amount_to_retrieve == "default":
            request = "/posts"
        else:
            request = f"/posts?amount={amount_to_retrieve}"
        response = client.get(request, headers=authorization.header)
        retrieved_posts = response.json()
        assert type(retrieved_posts) is list
        amount_to_retrieve = cast(int, 5 if amount_to_retrieve == "default" else amount_to_retrieve)
        if amount_to_create < amount_to_retrieve:
            assert len(retrieved_posts) == amount_to_create
        else:
            assert len(retrieved_posts) == amount_to_retrieve

    @pytest.mark.parametrize(
        "amount_to_create, amount_to_retrieve",
        [
            (10, 5), (2, 5)
        ]
    )
    def test_for_correct_amount_of_specified_author(
        self,
        authorization: AuthorizationData,
        amount_to_create: int, 
        amount_to_retrieve: int
    ) -> None:
        self.create_test_posts(test_posts[:amount_to_create], authorization)
        self.create_test_posts(
            test_posts[amount_to_create:],
            AuthorizationData(
                credentials={"username": "nutcracker", "password": "NutcrackerPassword123"}
            )
        )
        response = client.get(
            (
                "/posts?"
                f"author={authorization.credentials["username"]}&"
                f"amount={amount_to_retrieve}"
            ),
            headers=authorization.header
        )
        retrieved_posts = response.json()
        assert type(retrieved_posts) is list
        if amount_to_create < amount_to_retrieve:
            assert len(retrieved_posts) == amount_to_create
        else:
            assert len(retrieved_posts) == amount_to_retrieve

    @pytest.mark.parametrize(
        "amount_to_create, post_to_save_timestamp_after",
        [
            (5, 2),
            (5, 4),
            (10, 7)
        ]
    )
    def test_for_correct_timestamp(
        self,
        authorization: AuthorizationData,
        amount_to_create: int,
        post_to_save_timestamp_after: int
    ) -> None:
        for post_number in range(amount_to_create):
            client.post(
                "/posts",
                headers=authorization.header,
                json=test_posts[post_number]
            )
            if post_number == post_to_save_timestamp_after:
                until = datetime.now()
        response = client.get(
            f"/posts?until={until.isoformat()}",
            headers=authorization.header
        )
        retrieved_posts = response.json()
        assert type(retrieved_posts) is list
        expected_posts_amount = amount_to_create - post_to_save_timestamp_after
        assert len(retrieved_posts) == expected_posts_amount
        for post in retrieved_posts:
            post_timestamp = datetime.fromisoformat(post["timestamp"])
            assert post_timestamp < until