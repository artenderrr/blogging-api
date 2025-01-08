class AuthExampleRequests:
    register_credentials = {
        "normal": {
            "summary": "Valid registration credentials",
            "description": (
                "**Username:** Must be unique and at least 5 characters long.\n\n"
                "**Password:** Must be at least 8 characters long and contain both uppercase and lowercase letters."
            ),
            "value": {
                "username": "john_doe",
                "password": "SecurePassword2024"
            }
        },
        "invalid": {
            "summary": "Invalid registration credentials",
            "description": (
                "**Username:** Either already taken or less than 5 characters long.\n\n"
                "**Password:** Fails to meet the criteria of being at least 8 characters long or lacking either uppercase or lowercase letters."
            ),
            "value": {
                "username": "usr",
                "password": "short"
            }
        }
    }

    login_credentials = {
        "normal": {
            "summary": "Valid authentication credentials",
            "description": (
                "**Username:** Must represent an existing user's username.\n\n"
                "**Password:** Must match the password associated with the provided username."
            ),
            "value": {
                "username": "janeDoe",
                "password": "JaneDoeSecure2000"
            }
        },
        "invalid": {
            "summary": "Invalid authentication credentials",
            "description": (
                "**Username:** Does not represent an existing user's username.\n\n"
                "**Password:** Does not match the password associated with the provided username."
            ),
            "value": {
                "username": "nonExistentUser",
                "password": "WrongPassword123"
            }
        }
    }

class UserProfilesExampleRequests:
    username = {
        "normal": {
            "summary": "Valid username",
            "value": "existing_username"
        },
        "invalid": {
            "summary": "Invalid username",
            "value": "nonexistent_username"
        }
    }

    update_fields = {
        "normal": {
            "summary": "Valid update fields",
            "description": (
                "The request body must include at least one valid field defined in "
                "the `UserProfileUpdateFields` schema."
            ),
            "value": {
                "bio": "Backend Python Developer"
            }
        },
        "invalid": {
            "summary": "Invalid update fields",
            "description": (
                "Update fields are considered invalid if the request body is empty or "
                "contains only fields that do not match the valid fields defined in `UserProfileUpdateFields` schema."
            ),
            "value": {}
        }
    }

class PostsExampleRequests:
    new_post = {
        "normal": {
            "summary": "Valid post",
            "description": "A valid request must include both required fields: `title` and `content`.",
            "value": {
                "title": "My first post",
                "content": "Here are some contents of my first post!"
            }
        },
        "invalid": {
            "summary": "Invalid post",
            "description": "Post is considered invalid if the request body is missing one or both required fields: `title` and `content`.",
            "value": {}
        }
    }

    post_id = {
        "normal": {
            "summary": "Valid post ID",
            "value": 1
        },
        "invalid": {
            "summary": "Invalid post ID",
            "value": "nonexistent_id"
        }
    }

    update_fields = {
        "normal": {
            "summary": "Valid update fields",
            "description": (
                "The request body must include at least one valid field defined in "
                "the `PostUpdateFields` schema."
            ),
            "value": {
                "content": "Edited post content"
            }
        },
        "invalid": {
            "summary": "Invalid update fields",
            "description": (
                "Update fields are considered invalid if the request body is empty or "
                "contains only fields that do not match the valid fields defined in `PostUpdateFields` schema."
            ),
            "value": {}
        }
    }

    author = {
        "normal": {
            "summary": "Valid author",
            "value": "existing_username"
        },
        "invalid": {
            "summary": "Invalid author",
            "value": "nonexistent_username"
        }
    }

    until = {
        "normal": {
            "summary": "Valid timestamp",
            "value": "2025-01-08T11:50:54.404907"
        },
        "invalid": {
            "summary": "Invalid timestamp",
            "value": "today"
        }
    }

    amount = {
        "normal": {
            "summary": "Valid amount",
            "value": 10
        },
        "invalid": {
            "summary": "Invalid amount",
            "value": -1
        }
    }