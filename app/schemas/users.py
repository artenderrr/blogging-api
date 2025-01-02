from typing import Self
from pydantic import BaseModel, Field, model_validator

class UserProfile(BaseModel):
    username: str
    bio: str | None
    total_posts: int = Field(alias="totalPosts")

class UserProfileUpdateFields(BaseModel):
    bio: str | None = None

    @model_validator(mode="after")
    def require_at_least_one_field_present(self) -> Self:
        if not any(self.model_dump().values()):
            raise ValueError("At least one valid field must be provided")
        return self