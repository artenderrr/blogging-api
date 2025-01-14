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

class PostsExampleResponses:
    nonexistent_post = {
        "description": "Nonexistent Post",
        "content": {
            "application/json": {
                "example": {"detail": "Post with provided ID doesn't exist"}
            }
        }
    }

    restricted_access = {
        "description": "Restricted Access",
        "content": {
            "application/json": {
                "example": {"detail": "Post's ownership doesn't match the current user"}
            }
        }
    }

    nonexistent_author = {
        "description": "Nonexistent Author",
        "content": {
            "application/json": {
                "example": {"detail": "Author with provided username doesn't exist"}
            }
        }
    }

    invalid_timestamp = {
        "description": "Invalid Timestamp",
        "content": {
            "application/json": {
                "example": {"detail": "Provided timestamp is not a valid ISO 8601 format"}
            }
        }
    }