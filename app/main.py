from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.plaid_manager import PlaidManager
from app.schema import GetPlaidLinkTokenResponse, GetPlaidAccountsResponse

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
def get_plaid_link_token() -> GetPlaidLinkTokenResponse:
    """
    Get link token used by FE for plaid link component
    """
    link_token = plaid_manager.get_link_token()
    return GetPlaidLinkTokenResponse(plaid_link_token=link_token)


# TODO: This endpoint is doing too much.
# This needs to be broken into two endpoints.
# One: to exchange the public token for an access token which must be
# stored against the user in the database.
# Two: get account balances using the saved access token for the logged
# in user.
# The benefit of breaking it up is that then the access token can be
# re-used without forcing the user to relink to plaid for a new public
# token each time they request account balances.
# Later we will be able to use the access token to get other data from
# plaid like transactions
@app.get('/accounts')
def get_plaid_accounts(public_token: str) -> GetPlaidAccountsResponse:
    access_token = plaid_manager.exchange_public_token(public_token)
    accounts = plaid_manager.get_account_balances(access_token)
    return GetPlaidAccountsResponse.from_plaid_accounts(accounts)
