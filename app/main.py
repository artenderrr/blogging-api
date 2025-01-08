from fastapi import FastAPI
from app.routers import auth, users, posts

app = FastAPI(
    title="Blogging API",
    description="**Description:** API to interact with simple blogging platform.\n\n**Current state:** Stable.",
    version="1.0"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)