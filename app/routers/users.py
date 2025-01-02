from typing import Annotated
from fastapi import APIRouter, Depends
from app.schemas.users import UserProfile
from app.services.users import UsersService
from app.dependencies.users import existing_username
from app.dependencies.auth import get_current_user, verify_token

router = APIRouter()

@router.get("/users/me")
def get_current_user_profile(username: Annotated[str, Depends(get_current_user)]) -> UserProfile:
    user_profile = UsersService().get_profile(username)
    return user_profile

@router.get("/users/{username}", dependencies=[Depends(verify_token)])
def get_specific_user_profile(username: Annotated[str, Depends(existing_username)]) -> UserProfile:
    user_profile = UsersService().get_profile(username)
    return user_profile