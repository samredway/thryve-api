from fastapi import FastAPI

from app.plaid_manager import PlaidManager
from app.schema import GetPlaidLinkTokenResponse

app = FastAPI()
plaid_manager = PlaidManager()


@app.get("/")
def read_root() -> str:
    return "Server up!"


@app.get("/plaid-link-token")
def read_plaid_link_token() -> GetPlaidLinkTokenResponse:
    link_token = plaid_manager.get_link_token()
    return GetPlaidLinkTokenResponse(plaid_link_token=link_token)
