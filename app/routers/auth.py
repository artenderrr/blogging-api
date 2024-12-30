from typing import Annotated
from fastapi import APIRouter, Depends
from app.examples.responses import AuthExampleResponses
from app.services.auth import RegisterService, AuthenticateService
from app.dependencies.auth import valid_register_credentials, valid_login_credentials
from app.schemas.auth import BaseCredentials, RegisterCredentials, LoginCredentials, Token

router = APIRouter(tags=["Authentication"])

@router.post(
    "/register",
    summary="Create a new user account",
    responses={409: AuthExampleResponses.username_is_taken}
)
def register(
    credentials: Annotated[RegisterCredentials, Depends(valid_register_credentials)]
) -> BaseCredentials:
    RegisterService().create_credentials(credentials)
    return credentials

@router.post(
    "/login",
    summary="Authenticate an existing user account",
    responses={401: AuthExampleResponses.invalid_credentials}
)
def login(credentials: Annotated[LoginCredentials, Depends(valid_login_credentials)]) -> Token:
    access_token = AuthenticateService.create_access_token(credentials)
    return Token(access_token=access_token, token_type="bearer")