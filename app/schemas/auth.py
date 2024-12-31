from pydantic import BaseModel, Field, field_validator

class Token(BaseModel):
    access_token: str
    token_type: str

class BaseCredentials(BaseModel):
    username: str

class RegisterCredentials(BaseCredentials):
    username: str = Field(min_length=5)
    password: str = Field(min_length=8)

    @field_validator("password")
    @staticmethod
    def password_must_have_both_upper_and_lower_cases(password: str) -> str:
        if not next((i for i in password if i.islower()), None):
            raise ValueError("Password must contain at least one lowercase letter")
        elif not next((i for i in password if i.isupper()), None):
            raise ValueError("Password must contain at least one uppercase letter")
        return password
    
class LoginCredentials(BaseCredentials):
    password: str