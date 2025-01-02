from tinydb import TinyDB, where
from app.schemas.users import UserProfile

class UsersService:
    def __init__(self) -> None:
        self.users_db = TinyDB("app/db/users.json")

    def get_profile(self, username: str) -> UserProfile:
        user_profile = self.users_db.get(where("username") == username)
        return UserProfile(**user_profile)