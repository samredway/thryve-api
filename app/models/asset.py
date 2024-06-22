from app.models.base import Base
from app.models.mixins import PrimaryKeyMixin

from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import mapped_column, relationship


class Asset(Base, PrimaryKeyMixin):
    __tablename__ = "asset"

    type = mapped_column(String)
    name = mapped_column(String)
    value = mapped_column(Numeric(10, 2))
    user_id = mapped_column(ForeignKey("user.id"), index=True, nullable=False)

    user = relationship("User", back_populates="assets")
