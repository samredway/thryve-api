from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.base import Base
from app.models.mixins import PrimaryKeyMixin


class User(Base, PrimaryKeyMixin):
    __tablename__ = "user"

    cognito_id = mapped_column(UUID, unique=True, index=True)
    email = mapped_column(String, unique=True, index=True)
    cognito_refresh_token = mapped_column(String)
    plaid_access_token = mapped_column(String, default=None)

    assets = relationship("Asset", back_populates="user")
