import pytest
from app.plaid_manager import PlaidManager


@pytest.fixture
def plaid_manager() -> PlaidManager:
    return PlaidManager()


def test_token_retrieval(plaid_manager: PlaidManager) -> None:
    token = plaid_manager.get_link_token()
    assert token, "Token retrieval failed"
