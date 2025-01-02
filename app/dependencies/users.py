from typing import Annotated
from tinydb import TinyDB, where
from fastapi import Depends, HTTPException
from app.dependencies.common import db_connection

def existing_username(
    username: str,
    db: Annotated[TinyDB, Depends(db_connection("app/db/users.json"))]
) -> str:
    if not db.contains(where("username") == username):
        raise HTTPException(status_code=404, detail="User with provided username doesn't exist")
    return username