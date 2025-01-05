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
        retrieved_post["post_id"] = retrieved_post["postId"]
        retrieved_post.pop("postId")
        return PostWithMetaData(**retrieved_post)
    
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