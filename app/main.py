from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.plaid_manager import PlaidManager
from app.schema import GetPlaidLinkTokenResponse

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

plaid_manager = PlaidManager()


@app.get('/')
def read_root() -> str:
    return "Server up!"


@app.get('/plaid-link-token')
def read_plaid_link_token() -> GetPlaidLinkTokenResponse:
    link_token = plaid_manager.get_link_token()
    return GetPlaidLinkTokenResponse(plaid_link_token=link_token)
