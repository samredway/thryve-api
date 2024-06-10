from typing import Generator, Any, Annotated

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.services.auth.auth import verify_token
from app.services.auth.exceptions import AuthError
from app.database import SessionLocal


InvalidTokenError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token",
    headers={"WWW-Authenticate": "Bearer"},
)


def authorize(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise InvalidTokenError
    try:
        payload = verify_token(token)
        if payload is None:
            raise InvalidTokenError
    except AuthError:
        raise InvalidTokenError
    cognito_username: str = payload["username"]
    return cognito_username


AuthorizedUserDependency = Annotated[str, Depends(authorize)]


def get_session() -> Generator[Session, Any, Any]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


SessionDependency = Annotated[Session, Depends(get_session)]
