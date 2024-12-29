from pydantic import BaseModel, Field, field_validator

class BaseCredentials(BaseModel):
    username: str = Field(min_length=5)

class RegisterCredentials(BaseCredentials):
    password: str = Field(min_length=8)

    @field_validator("password")
    @staticmethod
    def password_must_have_both_upper_and_lower_cases(password: str) -> str:
        if not next((i for i in password if i.islower()), None):
            raise ValueError("Password must contain at least one lowercase letter")
        elif not next((i for i in password if i.isupper()), None):
            raise ValueError("Password must contain at least one uppercase letter")
        return password