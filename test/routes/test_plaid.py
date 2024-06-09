from unittest.mock import Mock, patch

from fastapi.testclient import TestClient


def test_get_plaid_link_token(client: TestClient) -> None:
    response = client.get('/plaid/link-token')
    assert response.status_code == 200
    assert response.json().get('plaid_link_token') is not None


@patch('app.services.plaid_manager.PlaidManager.exchange_public_token')
def test_get_plaid_accounts(mock_exchange_public_token: Mock, client: TestClient, access_token: str) -> None:
    mock_exchange_public_token.return_value = access_token
    response = client.get('/plaid/accounts?public_token=blah')
    assert response.status_code == 200
    assert response.json().get('accounts') is not None
