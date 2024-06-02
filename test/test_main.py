from fastapi.testclient import TestClient


def test_main(client: TestClient) -> None:
    response = client.get('/')
    assert response.status_code == 200


def test_read_plaid_link_token(client: TestClient) -> None:
    response = client.get('/plaid-link-token')
    assert response.status_code == 200
    assert response.json().get('plaid_link_token') is not None
