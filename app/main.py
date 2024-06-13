import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.routes.auth import router as auth_router
from app.routes.plaid import router as plaid_router
from app.models.base import Base

# import all models to create tables TODO: use alembic
from app.models.user import User  # noqa: F401

CLIENT_DOMAIN = os.environ.get("CLIENT_DOMAIN")

Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

origins = [CLIENT_DOMAIN]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(plaid_router)


@app.get("/")
async def read_root() -> str:
    """
    Check if the server is up
    """
    return "Server up!"
