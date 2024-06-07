import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.routes.plaid import router as plaid_router

load_dotenv()
URL_ROOT = os.environ.get('URL_ROOT')

app = FastAPI()

origins = [URL_ROOT]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(plaid_router)


@app.get('/')
async def read_root() -> str:
    """
    Check if the server is up
    """
    return "Server up!"
