from typing import Annotated, cast
import jwt
from jwt.exceptions import InvalidTokenError
import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from tinydb import TinyDB, where
from app.config import TokenConfig
from app.dependencies.common import db_connection
from app.schemas.auth import RegisterCredentials, LoginCredentials

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# validation dependencies

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


# authorization dependencies

def verify_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, str | int]:
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