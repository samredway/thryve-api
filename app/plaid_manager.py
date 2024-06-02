import os

from dotenv import load_dotenv
import plaid  # type: ignore
from plaid.api import plaid_api  # type: ignore
from plaid.model.link_token_create_request import LinkTokenCreateRequest  # type: ignore
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser  # type: ignore
from plaid.model.products import Products  # type: ignore
# from plaid.model.link_token_transactions import LinkTokenTransactions  # type: ignore
from plaid.model.country_code import CountryCode  # type: ignore


class PlaidManager:
    client: plaid_api.PlaidApi = None

    def __init__(self) -> None:
        self.initialise_plaid_client()

    def initialise_plaid_client(self) -> None:
        if PlaidManager.client is not None:
            return

        load_dotenv()
        client_id = os.getenv('PLAID_CLIENT_ID')
        secret = os.getenv('PLAID_SECRET')

        # Available environments are
        # 'Production'
        # 'Development'
        # 'Sandbox'
        configuration = plaid.Configuration(
            host=plaid.Environment.Sandbox,
            api_key={
                'clientId': client_id,
                'secret': secret,
            }
        )

        api_client = plaid.ApiClient(configuration)
        PlaidManager.client = plaid_api.PlaidApi(api_client)

    def get_link_token(self) -> str:
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(
                client_user_id='user-id',
                phone_number='+1 415 5550123'
            ),
            client_name='Personal Finance App',
            products=[Products('auth')],
            # Used with transactions product
            # transactions=LinkTokenTransactions(
            #     days_requested=730
            # ),
            country_codes=[CountryCode('GB')],
            language='en',

            # webhook is optional
            # webhook='https://sample-web-hook.com',

            # redirect_uri is required for OAuth with Plaid - must be set in the Plaid dashboard
            # redirect_uri='https://domainname.com/oauth-page.html',

            # Example of acount filters
            # account_filters=LinkTokenAccountFilters(
            #     depository=DepositoryFilter(
            #         account_subtypes=DepositoryAccountSubtypes([
            #             DepositoryAccountSubtype('checking'),
            #             DepositoryAccountSubtype('savings')
            #         ])
            #     ),
            #     credit=CreditFilter(
            #         account_subtypes=CreditAccountSubtypes([
            #             CreditAccountSubtype('credit card')
            #         ])
            #     )
            # )
        )

        response: dict[str, str] = PlaidManager.client.link_token_create(request)
        return response['link_token']
