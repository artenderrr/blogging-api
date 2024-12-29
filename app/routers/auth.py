from typing import Annotated
from fastapi import APIRouter, Depends
from app.services.auth import RegisterService, AuthenticateService
from app.dependencies.auth import valid_register_credentials, valid_login_credentials
from app.schemas.auth import BaseCredentials, RegisterCredentials, LoginCredentials, Token

router = APIRouter()

@router.post("/register")
def register(
    credentials: Annotated[RegisterCredentials, Depends(valid_register_credentials)]
) -> BaseCredentials:
    RegisterService().create_credentials(credentials)
    return credentials

@router.post("/login")
def login(credentials: Annotated[LoginCredentials, Depends(valid_login_credentials)]) -> Token:
    access_token = AuthenticateService.create_access_token(credentials)
    return Token(access_token=access_token, token_type="bearer")