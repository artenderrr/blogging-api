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