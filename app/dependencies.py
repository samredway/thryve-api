from typing import Generator, Any, Annotated

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.services.auth.auth import verify_token
from app.services.auth.exceptions import AuthError
from app.database import SessionLocal


invalid_token_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_session() -> Generator[Session, Any, Any]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


SessionDependency = Annotated[Session, Depends(get_session)]


def authorize(request: Request) -> str:  # TODO: should this return a User object?
    token = request.cookies.get("access_token")
    if not token:
        raise invalid_token_error
    try:
        payload = verify_token(token)
        if payload is None:
            raise invalid_token_error
    except AuthError:
        raise invalid_token_error
    cognito_id: str = payload["username"]

    if not cognito_id:
        raise invalid_token_error

    return cognito_id


AuthorizedUserDependency = Annotated[str, Depends(authorize)]
