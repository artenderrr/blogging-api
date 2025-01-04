from typing import Annotated
from fastapi import APIRouter, Body, Depends
from app.services.posts import PostsService
from app.dependencies.posts import existing_post_id
from app.dependencies.auth import get_current_user, verify_token
from app.schemas.posts import BasePost, PostWithMetaData
from app.examples.requests import PostsExampleRequests
from app.examples.responses import AuthExampleResponses, PostsExampleResponses

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

@router.get(
    "/posts/{post_id}",
    summary="Retrieve a specific post by its unique identifier",
    responses={
        401: AuthExampleResponses.invalid_token,
        404: PostsExampleResponses.nonexistent_post
    },
    dependencies=[Depends(verify_token)]
)
def retrieve_post(post_id: Annotated[int, Depends(existing_post_id)]) -> PostWithMetaData:
    retrieved_post = PostsService().retrieve_post(post_id)
    return retrieved_post