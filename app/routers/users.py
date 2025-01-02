from typing import Annotated
from fastapi import APIRouter, Depends
from app.services.users import UsersService
from app.dependencies.users import existing_username
from app.dependencies.auth import get_current_user, verify_token
from app.schemas.users import UserProfile, UserProfileUpdateFields

router = APIRouter()

@router.get("/users/me")
def get_current_user_profile(username: Annotated[str, Depends(get_current_user)]) -> UserProfile:
    user_profile = UsersService().get_profile(username)
    return user_profile

@router.get("/users/{username}", dependencies=[Depends(verify_token)])
def get_specific_user_profile(username: Annotated[str, Depends(existing_username)]) -> UserProfile:
    user_profile = UsersService().get_profile(username)
    return user_profile

@router.put("/users/me")
def update_current_user_profile(
    username: Annotated[str, Depends(get_current_user)],
    update_fields: UserProfileUpdateFields
) -> UserProfile:
    updated_user_profile = UsersService().update_profile(
        username,
        update_fields
    )
    return updated_user_profile