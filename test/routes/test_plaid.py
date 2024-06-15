from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from plaid.model.account_balance import AccountBalance  # type: ignore
from sqlalchemy.orm import Session

from app.models.user import User


def test_get_plaid_link_token(client: TestClient) -> None:
    response = client.get("/plaid/link-token")
    assert response.status_code == 200
    assert response.json().get("plaid_link_token") is not None


@patch("app.services.plaid.plaid_manager.PlaidManager.exchange_public_token")
def test_exchange_public_token(
    mock_exchange_public_token: Mock,
    client: TestClient,
    authorized_user: User,
    session: Session,
) -> None:
    """
    Test the access token gets saved to the user
    """
    mock_exchange_public_token.return_value = "New access token"
    response = client.post(
        "/plaid/exchange-public-token", json={"public_token": "New access token"}
    )
    assert response.status_code == 204
    session.get(User, authorized_user.id)
    assert authorized_user.plaid_access_token == "New access token"


@patch("app.services.plaid.plaid_manager.PlaidManager.get_account_balances")
def test_get_account_balances(
    mock_get_account_balances: Mock,
    client: TestClient,
    test_balances: list[AccountBalance],
) -> None:
    """
    The network call is mocked so we can smoke test that the endpoint
    is wired up correctly with and the validation is working
    """
    mock_get_account_balances.return_value = []
    response = client.get("/plaid/accounts")
    assert response.status_code == 200
    assert response.json().get("accounts") is not None


def test_get_account_balances_returns_403_if_no_access_token(
    client: TestClient, authorized_user: User, session: Session
) -> None:
    user = session.get(User, authorized_user.id)
    assert user
    user.plaid_access_token = "Invalid access token"
    session.commit()
    response = client.get("/plaid/accounts")
    assert response.status_code == 403
    assert response.json().get("detail") == "Invalid plaid access token"
