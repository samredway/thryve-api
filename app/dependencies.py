from typing import Generator, Any, Annotated

from fastapi import Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session

from app.services.auth.auth import verify_token, decode_token, refresh_token
from app.services.auth.exceptions import AuthError, ExpiredTokenError
from app.database import SessionLocal
from app.repositories.user import get_user_by_cognito_id

invalid_token_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token",
)


def get_session() -> Generator[Session, Any, Any]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


SessionDependency = Annotated[Session, Depends(get_session)]


def authorize(request: Request, session: SessionDependency, response: Response) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise invalid_token_error
    try:
        payload = verify_token(token)
        if payload is None:
            raise invalid_token_error
    except ExpiredTokenError:
        # If the token is expired, try to refresh it
        payload = decode_token(token)
        cognito_id: str = payload["username"]
        stmt = get_user_by_cognito_id(cognito_id)
        user = session.execute(stmt).scalar_one_or_none()
        if not user:
            raise invalid_token_error
        new_access_token = refresh_token(user.cognito_refresh_token)
        response.set_cookie(key="access_token", value=new_access_token, httponly=True)
        return cognito_id
    except AuthError:
        raise invalid_token_error

    # the cognito username is a uuid so in our app we use it as an id
    cognito_id = payload["username"]
    if not cognito_id:
        raise invalid_token_error

    return cognito_id


AuthorizedUserDependency = Annotated[str, Depends(authorize)]
