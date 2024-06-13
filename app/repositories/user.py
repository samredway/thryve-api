from sqlalchemy import select, Select

from app.models.user import User


def get_user_by_email(email: str) -> Select[tuple[User]]:
    stmt = select(User).where(User.email == email)
    return stmt


def get_user_by_cognito_id(cognito_id: str) -> Select[tuple[User]]:
    stmt = select(User).where(User.cognito_id == cognito_id)
    return stmt


def create_user(email: str, cognito_id: str, cognito_refresh_token: str) -> User:
    user: User = User(
        email=email,
        cognito_id=cognito_id,
        cognito_refresh_token=cognito_refresh_token,
    )
    return user
