from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    username: str
    bio: str | None
    total_posts: int = Field(alias="totalPosts")