from tinydb import TinyDB, where
from app.schemas.users import UserProfile, UserProfileUpdateFields

class UsersService:
    def __init__(self) -> None:
        self.users_db = TinyDB("app/db/users.json", indent=4)

    def get_profile(self, username: str) -> UserProfile:
        user_profile = self.users_db.get(where("username") == username)
        return UserProfile(**user_profile)
    
    def update_profile(
        self,
        username: str,
        update_fields: UserProfileUpdateFields
    ) -> UserProfile:
        self.users_db.update(update_fields, where("username") == username)
        updated_user_profile = self.get_profile(username)
        return updated_user_profile