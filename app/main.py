from fastapi import FastAPI
from app.routers import auth

app = FastAPI()

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World!"}

app.include_router(auth.router)