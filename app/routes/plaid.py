from fastapi import APIRouter

from app.services.plaid_manager import PlaidManager
from app.schemas.plaid import GetPlaidLinkTokenResponse, GetPlaidAccountsResponse


router = APIRouter(prefix="/plaid", tags=["plaid"])

plaid_manager = PlaidManager()


@router.get('/link-token')
async def get_plaid_link_token() -> GetPlaidLinkTokenResponse:
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
@router.get('/accounts')
async def get_plaid_accounts(public_token: str) -> GetPlaidAccountsResponse:
    access_token = plaid_manager.exchange_public_token(public_token)
    accounts = plaid_manager.get_account_balances(access_token)
    return GetPlaidAccountsResponse.from_plaid_accounts(accounts)
