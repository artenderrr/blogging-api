from typing import Annotated
from fastapi import APIRouter, Depends
from app.services.auth import RegisterService
from app.schemas.auth import BaseCredentials, RegisterCredentials
from app.dependencies.auth import valid_credentials

router = APIRouter()

@router.post("/register")
def register(credentials: Annotated[RegisterCredentials, Depends(valid_credentials)]) -> BaseCredentials:
    RegisterService().create_credentials(credentials)
    return credentials