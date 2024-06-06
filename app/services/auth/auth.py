import os

import requests

from app.exceptions import ConfigurationError
from app.services.auth.types_ import AuthTokens

cognito_domain = os.getenv('COGNITO_DOMAIN', '')
cognito_client_id = os.getenv('COGNITO_CLIENT_ID', '')
cognito_redirect_uri = os.getenv('COGNITO_REDIRECT_URI', '')

if not all([cognito_domain, cognito_client_id, cognito_redirect_uri]):
    raise ConfigurationError('Missing required environment variables for Cognito')


def exchange_code_for_tokens(code: str) -> AuthTokens:
    response = requests.post(
        cognito_domain,
        data={
            'grant_type': 'authorization_code',
            'client_id': cognito_client_id,
            'code': code,
            'redirect_uri': cognito_redirect_uri,
        },
    )
    response.raise_for_status()
    tokens = response.json()
    return AuthTokens(
        access_token=tokens['access_token'],
        refresh_token=tokens['refresh_token'],
        id_token=tokens['id_token'],
    )
