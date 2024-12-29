import bcrypt
from tinydb import TinyDB
from app.schemas.auth import RegisterCredentials

class RegisterService:
    def __init__(self) -> None:
        self.credentials_db = TinyDB("app/db/credentials.json", indent=4)

    @staticmethod
    def _hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")
        return hashed_password

    def create_credentials(self, credentials: RegisterCredentials) -> None:
        self.credentials_db.insert(
            {
                "username": credentials.username,
                "password": self._hash_password(credentials.password)
            }
        )