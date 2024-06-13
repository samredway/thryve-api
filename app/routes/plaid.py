from fastapi import APIRouter, HTTPException

from app.dependencies import AuthorizedUserDependency, SessionDependency
from app.repositories.user import get_user_by_cognito_id
from app.schemas.plaid import (
    PlaidPublicTokenExchangePostRequest,
    GetPlaidAccountsResponse,
    GetPlaidLinkTokenResponse,
)
from app.services.plaid.exceptions import InvalidAccessTokenError
from app.services.plaid.plaid_manager import PlaidManager

router = APIRouter(prefix="/plaid", tags=["Plaid"])

plaid_manager = PlaidManager()


@router.get("/link-token")
def get_plaid_link_token(
    cognito_id: AuthorizedUserDependency,
) -> GetPlaidLinkTokenResponse:
    """
    Get link token used by FE for plaid link component
    """
    link_token = plaid_manager.get_link_token()
    return GetPlaidLinkTokenResponse(plaid_link_token=link_token)


@router.post("/exchange-public-token", status_code=204)
def exchange_public_token(
    request_body: PlaidPublicTokenExchangePostRequest,
    cognito_id: AuthorizedUserDependency,
    session: SessionDependency,
) -> None:
    access_token = plaid_manager.exchange_public_token(request_body.public_token)
    stmt = get_user_by_cognito_id(cognito_id)
    user = session.execute(stmt).scalar_one()
    user.plaid_access_token = access_token
    session.commit()
    return None


@router.get("/accounts")
def get_plaid_account_balances(
    cognito_id: AuthorizedUserDependency, session: SessionDependency
) -> GetPlaidAccountsResponse:
    """
    Get plaid accounts for the logged in user
    """
    stmt = get_user_by_cognito_id(cognito_id)
    user = session.execute(stmt).scalar_one()
    if not user or not user.plaid_access_token:
        raise HTTPException(status_code=403, detail="No plaid access token")
    try:
        accounts = plaid_manager.get_account_balances(user.plaid_access_token)
    except InvalidAccessTokenError:
        raise HTTPException(status_code=403, detail="Invalid plaid access token")
    return GetPlaidAccountsResponse.from_plaid_accounts(accounts=accounts)
