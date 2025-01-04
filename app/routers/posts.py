from typing import Annotated
from fastapi import APIRouter, Body, Depends
from app.services.posts import PostsService
from app.dependencies.auth import get_current_user
from app.schemas.posts import BasePost, PostWithMetaData
from app.examples.requests import PostsExampleRequests
from app.examples.responses import AuthExampleResponses

router = APIRouter(tags=["Posts"])

@router.post(
    "/posts",
    status_code=201,
    summary="Create a new post authored by the currently authenticated user",
    responses={401: AuthExampleResponses.invalid_token}
)
def create_post(
    post: Annotated[BasePost, Body(
        openapi_examples=PostsExampleRequests.new_post
    )],
    username: Annotated[str, Depends(get_current_user)]
) -> PostWithMetaData:
    created_post = PostsService().create_post(
        title=post.title,
        author=username,
        content=post.content
    )
    return created_post