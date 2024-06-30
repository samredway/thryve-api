from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Response
import requests

from app.dependencies import AuthorizedUserDependency, SessionDependency
from app.repositories.user import get_user_by_cognito_id
from app.schemas.auth import LoginPostRequest, LoginPostResponse
from app.services.auth.auth import (
    exchange_code_for_tokens,
    verify_token,
    create_or_update_user_tokens,
)
from app.services.auth.exceptions import AuthError

import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    request_body: LoginPostRequest,
    response: Response,
    session: SessionDependency,
) -> LoginPostResponse:
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
            raise HTTPException(status_code=403, detail="Invalid code")
        raise HTTPException(
            status_code=500, detail="Failed to exchange code for tokens"
        )
    try:
        # verifying the access token only should be sufficient
        # verifying the id_token is a little more tricky
        access_token = verify_token(tokens.access_token)
    except AuthError:
        raise HTTPException(status_code=403, detail="Failed to verify token")

    cognito_id = access_token["username"]

    # create or update user in db with cognito username, email and refresh token
    user = create_or_update_user_tokens(cognito_id, tokens, session)

    # set the access token as an httpOnly cookie
    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True)

    return LoginPostResponse.model_validate({"user": asdict(user)})


@router.post("/logout", status_code=204)
def logout(
    response: Response,
    cognito_id: AuthorizedUserDependency,
    session: SessionDependency,
) -> None:
    """
    Logout clears the access token cookie and removes the refresh token
    from the database.
    """
    stmt = get_user_by_cognito_id(cognito_id)
    user = session.execute(stmt).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.cognito_refresh_token = None
    session.commit()
    response.delete_cookie(key="access_token")
    return None


@router.get("/me")
def get_me(user_id: AuthorizedUserDependency) -> dict[str, str]:
    """
    Returns the user info for authorized user
    """
    return {"cognito_id": user_id}
