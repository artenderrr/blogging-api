from typing import Annotated
from fastapi import FastAPI, Depends
from app.routers import auth
from app.dependencies.auth import get_current_user

app = FastAPI()

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World!"}

@app.get("/protected")
def protected(
    username: Annotated[str, Depends(get_current_user)]
) -> dict[str, str]:
    return {"message": f"Hello, {username}!"}

app.include_router(auth.router)