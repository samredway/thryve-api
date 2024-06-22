from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column


class PrimaryKeyMixin:
    id = mapped_column(BigInteger, primary_key=True)
