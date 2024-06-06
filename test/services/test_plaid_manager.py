import pytest
from app.services.plaid_manager import PlaidManager
from plaid.model.account_base import AccountBase  # type: ignore


@pytest.fixture
def plaid_manager() -> PlaidManager:
    return PlaidManager()


def test_token_retrieval(plaid_manager: PlaidManager) -> None:
    token = plaid_manager.get_link_token()
    assert token


def test_get_account_balances(
        plaid_manager: PlaidManager,
        access_token: str,
        test_balances: list[AccountBase],
) -> None:
    balances = plaid_manager.get_account_balances(access_token)
    for balance in balances:
        assert isinstance(balance, AccountBase)
        assert balance == test_balances.pop(0)
