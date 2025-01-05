from typing import Self
from pydantic import BaseModel, Field, model_validator

class BasePost(BaseModel):
    title: str
    content: str

class PostWithMetaData(BasePost):
    post_id: int = Field(serialization_alias="postId")
    author: str
    timestamp: str

class PostUpdateFields(BaseModel):
    title: str | None = None
    content: str | None = None

    @model_validator(mode="after")
    def require_at_least_one_field_present(self) -> Self:
        if not any(self.model_dump().values()):
            raise ValueError("At least one valid field must be provided")
        return self