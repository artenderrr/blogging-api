from typing import Annotated
from app.services.users import UsersService
from fastapi import APIRouter, Depends, Body
from app.dependencies.users import existing_username
from app.dependencies.auth import get_current_user, verify_token
from app.schemas.users import UserProfile, UserProfileUpdateFields
from app.examples.requests import UserProfilesExampleRequests
from app.examples.responses import AuthExampleResponses, UserProfilesExampleResponses

router = APIRouter(tags=["Users"])

@router.get(
    "/users/me",
    summary="Retrieve the profile of the currently authenticated user",
    responses={401: AuthExampleResponses.invalid_token}
)
def get_current_user_profile(username: Annotated[str, Depends(get_current_user)]) -> UserProfile:
    user_profile = UsersService().get_profile(username)
    return user_profile

@router.put(
    "/users/me",
    summary="Update the profile of the currently authenticated user",
    responses={401: AuthExampleResponses.invalid_token}
)
def update_current_user_profile(
    username: Annotated[str, Depends(get_current_user)],
    update_fields: Annotated[UserProfileUpdateFields, Body(
        openapi_examples=UserProfilesExampleRequests.update_fields
    )]
) -> UserProfile:
    updated_user_profile = UsersService().update_profile(
        username,
        update_fields
    )
    return updated_user_profile

@router.get(
    "/users/{username}",
    summary="Retrieve the profile of a specific user by username",
    responses={
        401: AuthExampleResponses.invalid_token,
        404: UserProfilesExampleResponses.nonexistent_user
    },
    dependencies=[Depends(verify_token)]
)
def get_specific_user_profile(username: Annotated[str, Depends(existing_username)]) -> UserProfile:
    user_profile = UsersService().get_profile(username)
    return user_profile