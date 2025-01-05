from typing import Annotated, cast
from tinydb import TinyDB, where
from fastapi import Path, Depends, HTTPException
from app.dependencies.common import db_connection
from app.examples.requests import PostsExampleRequests

def existing_post_id(
    post_id: Annotated[int, Path(
        gt=0,
        description="A unique identifier of an existing post whose data is being requested.",
        openapi_examples=PostsExampleRequests.post_id
    )],
    db: Annotated[TinyDB, Depends(db_connection("app/db/posts.json"))]
) -> int:
    if not db.contains(where("postId") == post_id):
        raise HTTPException(status_code=404, detail="Post with provided ID doesn't exist")
    return post_id

def post_ownership_matches_current_user(post_id: int, username: str) -> bool:
    db = TinyDB("app/db/posts.json")
    post_author = cast(str, db.get(where("postId") == post_id)["author"])
    return post_author == username