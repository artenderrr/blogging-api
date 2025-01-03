class AuthExampleResponses:
    username_is_taken = {
        "description": "Username is Taken",
        "content": {
            "application/json": {
                "example": {"detail": "Provided username is taken"}
            }
        }
    }

    invalid_credentials = {
        "description": "Invalid Credentials",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid credentials"}
            }
        }
    }

    invalid_token = {
        "description": "Invalid Token",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid or expired token"}
            }
        }
    }

class UserProfilesExampleResponses:
    nonexistent_user = {
        "description": "Nonexistent User",
        "content": {
            "application/json": {
                "example": {"detail": "User with provided username doesn't exist"}
            }
        }
    }