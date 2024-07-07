import json
import os

import plaid  # type: ignore
from plaid.api import plaid_api  # type: ignore
from plaid.model.link_token_create_request import LinkTokenCreateRequest  # type: ignore
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser  # type: ignore
from plaid.model.products import Products  # type: ignore
from plaid.model.country_code import CountryCode  # type: ignore
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest  # type: ignore
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest  # type: ignore

from app.schemas.plaid import PlaidAccount
from app.services.plaid.exceptions import InvalidAccessTokenError, PlaidError


class PlaidManager:
    """
    PlaidManager is a state manager designed to hold a single instance of the plaid client across
    mutliple runs without rehitting the plaid api.

    At some point we might want to have a more organised results cache and limit hits on the balance
    endpoint as these are PAYG access.
    """

    _client: plaid_api.PlaidApi | None = None

    def __init__(self) -> None:
        if self._client:
            return
        self.initialise_plaid_client()

    @staticmethod
    def _get_client() -> plaid_api.PlaidApi:
        if not PlaidManager._client:
            raise ValueError("Plaid client is not intialised")
        return PlaidManager._client

    def initialise_plaid_client(self) -> None:
        client_id = os.getenv("PLAID_CLIENT_ID")
        secret = os.getenv("PLAID_SECRET")

        if not client_id or not secret:
            raise ValueError(
                "Plaid client_id and secret must be set in the environment variables"
            )

        configuration = plaid.Configuration(
            host=plaid.Environment.Sandbox,
            api_key={
                "clientId": client_id,
                "secret": secret,
            },
        )
        api_client = plaid.ApiClient(configuration)
        PlaidManager._client = plaid_api.PlaidApi(api_client)

    def get_link_token(self) -> str:
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id="user-id"),
            client_name="Personal Finance App",
            products=[Products("auth")],
            country_codes=[CountryCode("GB")],
            language="en",
        )
        response: dict[str, str] = PlaidManager._get_client().link_token_create(request)
        return response["link_token"]

    def exchange_public_token(self, public_token: str) -> str:
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = PlaidManager._get_client().item_public_token_exchange(request)
        if not isinstance(access_token := response.get("access_token"), str):
            raise PlaidError("Access token not found in Plaid response")
        return access_token

    def get_account_balances(self, access_token: str) -> list[PlaidAccount]:
        request = AccountsBalanceGetRequest(access_token=access_token)
        try:
            response = PlaidManager._get_client().accounts_balance_get(request)
        except plaid.ApiException as err:
            body = json.loads(err.body)
            if body.get("error_code") == "INVALID_ACCESS_TOKEN":
                raise InvalidAccessTokenError()
            raise PlaidError(body["error_message"])
        accounts = response["accounts"]
        return [
            # Note using the external schema class internally here to avoid
            # duplication by creating an internal dataclass model
            PlaidAccount.from_plaid_account_balance_raw(account)
            for account in accounts
        ]
