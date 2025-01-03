from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
from tinydb import TinyDB
from app.config import TokenConfig
from app.schemas.auth import RegisterCredentials, LoginCredentials

class RegisterService:
    def __init__(self, credentials: RegisterCredentials) -> None:
        self.credentials = credentials
        self.credentials_db = TinyDB("app/db/credentials.json", indent=4)
        self.users_db = TinyDB("app/db/users.json", indent=4)

    @staticmethod
    def _hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")
        return hashed_password

    def _create_credentials(self) -> None:
        self.credentials_db.insert(
            {
                "username": self.credentials.username,
                "password": self._hash_password(self.credentials.password)
            }
        )
    
    def _create_user(self) -> None:
        self.users_db.insert(
            {
                "username": self.credentials.username,
                "bio": None,
                "totalPosts": 0
            }
        )

    def register_user(self) -> None:
        self._create_credentials()
        self._create_user()

class AuthenticateService:
    @staticmethod
    def create_access_token(credentials: LoginCredentials) -> str:
        payload = {
            "sub": credentials.username,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=TokenConfig.EXPIRE_SECONDS)
        }
        access_token = jwt.encode(payload, TokenConfig.SECRET_KEY, algorithm=TokenConfig.ALGORITHM)
        return access_token