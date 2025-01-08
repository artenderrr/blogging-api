from typing import Annotated, cast
from datetime import datetime
from tinydb import TinyDB, where
from fastapi import Path, Query, Depends, HTTPException
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

def is_valid_timestamp(timestamp: str) -> bool:
    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False

def valid_until_parameter(
    until: Annotated[str, Query(
        description=(
            "A timestamp in ISO 8601 format indicating the cut-off point, "
            "retrieving posts created before the specified moment in time."
        ),
        openapi_examples=PostsExampleRequests.until,
        default_factory=lambda: datetime.now().isoformat()
    )]
) -> str:
    if not is_valid_timestamp(until):
        raise HTTPException(status_code=400, detail="Provided timestamp is not a valid ISO 8601 format")
    return until

def existing_author(
    db: Annotated[TinyDB, Depends(db_connection("app/db/users.json"))],
    author: Annotated[str | None, Query(
        description="The username of the user whose posts should be retrieved.",
        openapi_examples=PostsExampleRequests.author
    )] = None
) -> str | None:
    if author and not db.contains(where("username") == author):
        raise HTTPException(status_code=404, detail="Author with provided username doesn't exist")
    return author