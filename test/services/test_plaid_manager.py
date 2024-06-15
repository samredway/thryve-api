from plaid.model.account_base import AccountBase  # type: ignore

import pytest

from app.schemas.plaid import PlaidAccount
from app.services.plaid.plaid_manager import PlaidManager


@pytest.fixture
def plaid_manager() -> PlaidManager:
    return PlaidManager()


def test_token_retrieval(plaid_manager: PlaidManager) -> None:
    token = plaid_manager.get_link_token()
    assert token


def test_get_account_balances(
    plaid_manager: PlaidManager,
    plaid_access_token: str,
    test_balances: list[AccountBase],
) -> None:
    balances = plaid_manager.get_account_balances(plaid_access_token)
    for balance in balances:
        assert isinstance(balance, PlaidAccount)
        assert balance == PlaidAccount.from_plaid_account_balance_raw(
            test_balances.pop(0)
        )
