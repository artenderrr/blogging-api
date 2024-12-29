from typing import Annotated
import bcrypt
from fastapi import Depends, HTTPException
from tinydb import TinyDB, where
from app.dependencies.common import db_connection
from app.schemas.auth import RegisterCredentials, LoginCredentials

def valid_register_credentials(
    credentials: RegisterCredentials,
    db: Annotated[TinyDB, Depends(db_connection("app/db/credentials.json"))]
) -> RegisterCredentials:
    if db.contains(where("username") == credentials.username):
        raise HTTPException(status_code=409, detail="Provided username is taken")
    return credentials

def valid_login_credentials(
    credentials: LoginCredentials,
    db: Annotated[TinyDB, Depends(db_connection("app/db/credentials.json"))]
) -> LoginCredentials:
    if (
        not db.contains(where("username") == credentials.username)
        or
        not bcrypt.checkpw(
            credentials.password.encode("utf-8"),
            db.get(where("username") == credentials.username).get("password").encode("utf-8")
        )
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials