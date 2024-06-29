import os
from typing import Any

from jose import jwt, jwk
from jose.exceptions import JWTClaimsError, JWTError
from jose.utils import base64url_decode
import requests
from sqlalchemy.orm import Session

from app.exceptions import ConfigurationError
from app.repositories.user import get_user_by_email, create_user
from app.services.auth.types_ import AuthTokens
from app.services.auth.exceptions import AuthError
from app.types_ import User

cognito_domain = os.getenv("COGNITO_DOMAIN", "")
cognito_client_id = os.getenv("COGNITO_CLIENT_ID", "")
cognito_redirect_uri = os.getenv("COGNITO_REDIRECT_URI", "")
jwks_url = os.getenv("COGNITO_JWKS_URL", "")

if not all([cognito_domain, cognito_client_id, cognito_redirect_uri, jwks_url]):
    raise ConfigurationError("Missing required environment variables for Cognito")


def exchange_code_for_tokens(code: str) -> AuthTokens:
    response = requests.post(
        cognito_domain + "/oauth2/token",
        data={
            "grant_type": "authorization_code",
            "client_id": cognito_client_id,
            "code": code,
            "redirect_uri": cognito_redirect_uri,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    tokens = response.json()
    return AuthTokens(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        id_token=tokens["id_token"],
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode a JWT token without verifying its signature
    """
    payload: dict[str, Any] = jwt.get_unverified_claims(token)
    return payload


def verify_token(token: str) -> dict[str, Any]:
    response = requests.get(jwks_url)
    jwks: dict[str, Any] = response.json()

    try:
        headers: dict[str, Any] = jwt.get_unverified_header(token)
    except JWTError:
        raise AuthError("Invalid token header")

    kid: str = headers["kid"]
    key: dict[str, Any] = next(key for key in jwks["keys"] if key["kid"] == kid)
    public_key = jwk.construct(key)
    message, encoded_signature = token.rsplit(".", 1)
    decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))

    if not public_key.verify(message.encode("utf-8"), decoded_signature):
        raise AuthError("Invalid token signature")

    try:
        decoded_token = jwt.decode(
            token, public_key, algorithms=["RS256"], audience=cognito_client_id
        )
    except JWTClaimsError:
        raise AuthError("Invalid token claims")

    return decoded_token


def create_or_update_user_tokens(
    cognito_id: str, tokens: AuthTokens, session: Session
) -> User:
    id_token = decode_token(tokens.id_token)
    email = id_token["email"]

    stmt = get_user_by_email(email)
    user = session.execute(stmt).scalar()
    if not user:
        user = create_user(
            email=email,
            cognito_id=cognito_id,
            cognito_refresh_token=tokens.refresh_token,
        )
        session.add(user)
    else:
        user.cognito_refresh_token = tokens.refresh_token

    session.commit()

    return User(id=user.id, email=email)


def refresh_token(refresh_token: str) -> AuthTokens:
    response = requests.post(
        cognito_domain + "/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "client_id": cognito_client_id,
            "refresh_token": refresh_token,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    tokens = response.json()
    return AuthTokens(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        id_token=tokens["id_token"],
    )
