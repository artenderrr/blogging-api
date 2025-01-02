from typing import Annotated
from fastapi import APIRouter, Depends
from app.schemas.users import UserProfile
from app.services.users import UsersService
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/users/me")
def get_current_user_profile(username: Annotated[str, Depends(get_current_user)]) -> UserProfile:
    user_profile = UsersService().get_profile(username)
    return user_profile