from fastapi import APIRouter, HTTPException
import requests

from app.schemas.auth import LoginPostRequest
from app.services.auth.auth import (
    exchange_code_for_tokens,
    verify_token,
    decode_token,
    #create_http_only_cookie,
)
from app.services.auth.exceptions import AuthError

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/login')
def login(request_body: LoginPostRequest) -> None:
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

    id_token = decode_token(tokens.id_token)

    username = access_token['username']
    email = id_token['email']

    print(username, email)

    # create or update user in db with email and refresh token

    # cookie = create_http_only_cookie(tokens.access_token)
    # return user object and set cookie
    return
