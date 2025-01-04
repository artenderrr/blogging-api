from datetime import datetime
from tinydb import TinyDB
from app.schemas.posts import PostWithMetaData

class PostsService:
    def __init__(self) -> None:
        self.posts_db = TinyDB("app/db/posts.json", indent=4)

    def create_post(self, title: str, author: str, content: str) -> PostWithMetaData:
        post = {
            "title": title,
            "author": author,
            "content": content,
            "timestamp": self._generate_timestamp()
        }
        post_id = self.posts_db.insert(post)
        self.posts_db.update({"postId": post_id}, doc_ids=[post_id])
        return PostWithMetaData(**post, post_id=post_id)

    def _generate_timestamp(self) -> str:
        return datetime.now().isoformat()