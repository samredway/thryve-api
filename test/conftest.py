import pytest
from fastapi.testclient import TestClient
from plaid.model.account_base import AccountBase  # type: ignore
from plaid.model.account_balance import AccountBalance  # type: ignore
from plaid.model.account_type import AccountType  # type: ignore
from plaid.model.account_subtype import AccountSubtype  # type: ignore

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def access_token() -> str:
    return 'access-sandbox-bed183dd-4a59-438f-8116-e8761c83bb1d'


@pytest.fixture
def test_balances() -> list[AccountBase]:
    return [
        AccountBase(
            account_id='mvoQKZNRWNuLve75A4MKhR6ZNj5VENCgexdnQ',
            balances=AccountBalance(
                available=100.0,
                current=110.0,
                iso_currency_code='GBP',
                limit=None,
                unofficial_currency_code=None
            ),
            mask='0000',
            name='Plaid Current Account',
            official_name='Plaid Standard Current Account',
            persistent_account_id='8cfb8beb89b774ee43b090625f0d61d0814322b43bff984eaf60386e',
            subtype=AccountSubtype('checking'),
            type=AccountType('depository'),
        ),
        AccountBase(
            account_id='ywvG7zgN9gC6wJ5Z1DyzuaPwdrQWZdt4PjXbP',
            balances=AccountBalance(
                available=200.0,
                current=210.0,
                iso_currency_code='GBP',
                limit=None,
                unofficial_currency_code=None
            ),
            mask='1111',
            name='Plaid Saving',
            official_name='Plaid Standard Interest Saving',
            persistent_account_id='211a4e5d8361a3afb7a3886362198c7306e00a313b5aa944c20d34b6',
            subtype=AccountSubtype('savings'),
            type=AccountType('depository'),
        ),
        AccountBase(
            account_id='9J4qzNe1Weu8PXDE9Gy1szA8LNwdjLu4oAQwy',
            balances=AccountBalance(
                available=None,
                current=410.0,
                iso_currency_code='GBP',
                limit=2000.0,
                unofficial_currency_code=None
            ),
            mask='3333',
            name='Plaid Credit Card',
            official_name='Plaid Diamond Credit Card',
            subtype=AccountSubtype('credit card'),
            type=AccountType('credit'),
        ),
        AccountBase(
            account_id='vvmEN9LdbLulv6qDnrpRF5bQx3DeGxHqbNkB6',
            balances=AccountBalance(
                available=None,
                current=56302.06,
                iso_currency_code='GBP',
                limit=None,
                unofficial_currency_code=None
            ),
            mask='8888',
            name='Plaid Mortgage',
            official_name=None,
            subtype=AccountSubtype('mortgage'),
            type=AccountType('loan'),
        ),
    ]
