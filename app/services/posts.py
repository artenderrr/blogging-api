from typing import cast
from datetime import datetime
from tinydb import TinyDB, where
from tinydb.operations import increment, decrement
from app.schemas.posts import PostWithMetaData, PostUpdateFields

class PostsService:
    def __init__(self) -> None:
        self.posts_db = TinyDB("app/db/posts.json", indent=4)
        self.users_db = TinyDB("app/db/users.json", indent=4)

    def create_post(self, title: str, author: str, content: str) -> PostWithMetaData:
        post = {
            "title": title,
            "author": author,
            "content": content,
            "timestamp": PostsService._generate_timestamp()
        }
        post_id = self.posts_db.insert(post)
        self.posts_db.update({"postId": post_id}, doc_ids=[post_id])
        self._increment_author_total_posts(author)
        return PostWithMetaData(**post, post_id=post_id)
    
    def _increment_author_total_posts(self, author: str) -> None:
        self.users_db.update(increment("totalPosts"), where("username") == author) # type: ignore

    @staticmethod
    def _generate_timestamp() -> str:
        return datetime.now().isoformat()
    
    def retrieve_post(self, post_id: int) -> PostWithMetaData:
        retrieved_post = self.posts_db.get(where("postId") == post_id)
        retrieved_post = self._swap_post_id_keys([retrieved_post])[0]
        return PostWithMetaData(**retrieved_post)
    
    def retrieve_posts(
        self,
        author: str | None,
        until: str,
        amount: int
    ) -> list[PostWithMetaData]:
        retrieved_posts = self._retrieve_posts_until_timestamp(until)
        posts_with_post_id_keys_swapped = self._swap_post_id_keys(retrieved_posts)
        if author:
            retrieved_posts = filter(
                lambda post: post["author"] == author,
                posts_with_post_id_keys_swapped
            )
        retrieved_posts = self._sort_posts_by_timestamp(retrieved_posts)
        return retrieved_posts[:amount]
    
    def _retrieve_posts_until_timestamp(self, until: str) -> list[PostWithMetaData]:
        retrieved_posts = self.posts_db.search(
            where("timestamp").test(lambda timestamp: (
                datetime.fromisoformat(timestamp)
                <
                datetime.fromisoformat(until)
            ))
        )
        return retrieved_posts
    
    def _sort_posts_by_timestamp(self, posts: list[PostWithMetaData]) -> list[PostWithMetaData]:
        sorted_posts = sorted(posts, key=lambda post: (
            datetime.fromisoformat(post["timestamp"])
        ), reverse=True)
        return sorted_posts
    
    def _swap_post_id_keys(self, posts: list[PostWithMetaData]) -> list[PostWithMetaData]:
        copied_posts = posts.copy()
        for post in copied_posts:
            post["post_id"] = post["postId"]
            post.pop("postId")
        return copied_posts
    
    def edit_post(self, post_id: int, update_fields: PostUpdateFields) -> PostWithMetaData:
        self.posts_db.update(
            update_fields.model_dump(exclude_unset=True),
            where("postId") == post_id
        )
        return self.retrieve_post(post_id)
    
    def delete_post(self, post_id: int) -> None:
        author = self._get_post_author(post_id)
        self._decrement_author_total_posts(author)
        self.posts_db.remove(where("postId") == post_id)

    def _get_post_author(self, post_id: int) -> str:
        post = self.posts_db.get(where("postId") == post_id)
        author = cast(str, post["author"])
        return author
    
    def _decrement_author_total_posts(self, author: str) -> None:
        self.users_db.update(decrement("totalPosts"), where("username") == author) # type: ignore