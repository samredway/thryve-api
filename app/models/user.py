from sqlalchemy import BigInteger, String
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class User(Base):
    __tablename__ = "user"

    id = mapped_column(BigInteger, primary_key=True)
    email = mapped_column(String, unique=True, index=True)
    username = mapped_column(String, default=None)
    cognito_username = mapped_column(String)
    cognito_refresh_token = mapped_column(String)
    plaid_access_token = mapped_column(String, default=None)
