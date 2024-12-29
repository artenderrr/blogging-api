from typing import Annotated
from fastapi import Depends, HTTPException
from tinydb import TinyDB, where
from app.schemas.auth import RegisterCredentials
from app.dependencies.common import db_connection

def valid_credentials(
        credentials: RegisterCredentials,
        db: Annotated[TinyDB, Depends(db_connection("app/db/credentials.json"))]
) -> RegisterCredentials:
    if db.contains(where("username") == credentials.username):
        raise HTTPException(status_code=409, detail="Provided username is taken")
    return credentials