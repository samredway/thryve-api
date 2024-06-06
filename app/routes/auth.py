from fastapi import APIRouter

from app.schemas.auth import LoginPostRequest
from app.services.auth.auth import exchange_code_for_tokens, create_http_only_cookie

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/login')
def login(request_body: LoginPostRequest) -> None:
    """
    Login swaps the code for a token by sending off to cognito.

    If the user does not exist in the database, it creates a new user object.

    It stores the token in and httpOnly cookie and returns the user object, and
    retains the refresh token in the database.
    """
    tokens = exchange_code_for_tokens(request_body.code)
    # cookie = create_http_only_cookie(tokens.access_token)
    # extract email from id token
    # create or update user in db with email and refresh token
    # return user object and set cookie
    return
