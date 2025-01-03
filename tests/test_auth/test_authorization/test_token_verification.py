import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.dependencies.auth import verify_token
from tests.utils import AuthorizationData

@pytest.mark.parametrize(
    "authorization",
    [
        {"username": "john_doe", "password": "SuperSecret"},
        {"username": "JaneDoe", "password": "LoremIpsum"},
        {"username": "mysterious_hacker", "password": "LiterallyUnhackablePassword"}
    ],
    indirect=True
)
def test_verification_of_valid_token(authorization: AuthorizationData) -> None:
    payload = verify_token(
        HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=authorization.token
        )
    )
    assert type(payload) is dict
    assert len(payload) == 2
    assert all(claim in payload for claim in ("sub", "exp"))
    assert payload["sub"] == authorization.credentials["username"]

def test_verification_of_invalid_token() -> None:
    with pytest.raises(HTTPException) as excinfo:
        verify_token(
            HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials="invalid_token"
            )
        )
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid or expired token"