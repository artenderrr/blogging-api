from typing import Annotated
from tinydb import TinyDB, where
from fastapi import Path, Depends, HTTPException
from app.dependencies.common import db_connection
from app.examples.requests import UserProfilesExampleRequests

def existing_username(
    username: Annotated[str, Path(
        description="The username of an existing user whose profile data is being requested.",
        openapi_examples=UserProfilesExampleRequests.username
    )],
    db: Annotated[TinyDB, Depends(db_connection("app/db/users.json"))]
) -> str:
    if not db.contains(where("username") == username):
        raise HTTPException(status_code=404, detail="User with provided username doesn't exist")
    return username