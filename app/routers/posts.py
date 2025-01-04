from typing import Annotated
from fastapi import APIRouter, Depends
from app.services.posts import PostsService
from app.dependencies.auth import get_current_user
from app.schemas.posts import BasePost, PostWithMetaData

router = APIRouter()

@router.post("/posts", status_code=201)
def create_post(
    post: BasePost,
    username: Annotated[str, Depends(get_current_user)]
) -> PostWithMetaData:
    created_post = PostsService().create_post(
        title=post.title,
        author=username,
        content=post.content
    )
    return created_post