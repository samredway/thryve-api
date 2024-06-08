from dataclasses import asdict

from fastapi import APIRouter, HTTPException
import requests

from app.dependencies import SessionDependency
from app.schemas.auth import LoginPostRequest, LoginPostResponse
from app.services.auth.auth import (
    exchange_code_for_tokens,
    verify_token,
    create_or_update_user_tokens,
)
from app.services.auth.exceptions import AuthError

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/login')
async def login(request_body: LoginPostRequest, session: SessionDependency) -> LoginPostResponse:
    """
    Login swaps the code for a token by sending off to cognito.

    If the user does not exist in the database, it creates a new user object.

    It stores the token in and httpOnly cookie and returns the user object, and
    retains the refresh token in the database.
    """
    try:
        tokens = exchange_code_for_tokens(request_body.code)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            raise HTTPException(status_code=403, detail='Invalid code')
        raise HTTPException(status_code=500, detail='Failed to exchange code for tokens')
    try:
        # verifying the access token only should be sufficient
        # verifying the id_token is a little more tricky
        access_token = verify_token(tokens.access_token)
    except AuthError:
        raise HTTPException(status_code=403, detail='Failed to verify token')

    cognito_username = access_token['username']

    # create or update user in db with email and refresh token
    user = create_or_update_user_tokens(cognito_username, tokens, session)

    # TODO cookie = create_http_only_cookie(tokens.access_token)
    # return user object and set cookie
    return LoginPostResponse.model_validate({'user': asdict(user)})
