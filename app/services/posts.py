from datetime import datetime
from tinydb import TinyDB, where
from tinydb.operations import increment
from app.schemas.posts import PostWithMetaData

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