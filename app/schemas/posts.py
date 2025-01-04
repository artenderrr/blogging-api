from pydantic import BaseModel, Field

class BasePost(BaseModel):
    title: str
    content: str

class PostWithMetaData(BasePost):
    post_id: int = Field(serialization_alias="postId")
    author: str
    timestamp: str