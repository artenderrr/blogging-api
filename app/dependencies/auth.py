from typing import Annotated, cast
import jwt
from jwt.exceptions import InvalidTokenError
import bcrypt
from fastapi import Body, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from tinydb import TinyDB, where
from app.config import TokenConfig
from app.examples.requests import AuthExampleRequests
from app.dependencies.common import db_connection
from app.schemas.auth import RegisterCredentials, LoginCredentials

security = HTTPBearer()


# validation dependencies

def valid_register_credentials(
    credentials: Annotated[RegisterCredentials, Body(
        openapi_examples=AuthExampleRequests.register_credentials
    )],
    db: Annotated[TinyDB, Depends(db_connection("app/db/credentials.json"))]
) -> RegisterCredentials:
    if db.contains(where("username") == credentials.username):
        raise HTTPException(status_code=409, detail="Provided username is taken")
    return credentials

def valid_login_credentials(
    credentials: Annotated[LoginCredentials, Body(
        openapi_examples=AuthExampleRequests.login_credentials
    )],
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


# authorization dependencies

def verify_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict[str, str | int]:
    token = credentials.credentials
    try:
        payload = cast(
            dict[str, str | int],
            jwt.decode(token, TokenConfig.SECRET_KEY, algorithms=[TokenConfig.ALGORITHM])
        )
        return payload
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
def get_current_user(payload: Annotated[dict[str, str | int], Depends(verify_token)]) -> str:
    username = cast(str, payload["sub"])
    return username