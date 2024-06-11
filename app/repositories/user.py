from sqlalchemy import select, Select

from app.models.user import User


def get_user_by_email(email: str) -> Select[tuple[User]]:
    stmt = select(User).where(User.email == email)
    return stmt


def create_user(email: str, cognito_username: str, cognito_refresh_token: str) -> User:
    user: User = User(
        email=email,
        cognito_username=cognito_username,
        cognito_refresh_token=cognito_refresh_token,
    )
    return user
