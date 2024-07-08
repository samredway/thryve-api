from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from app.schemas.base import BaseSchema


class AssetType(StrEnum):
    crypto = "crypto"
    stocks = "stocks"
    property = "property"
    cash = "cash"
    loan = "loan"
    other = "other"


class AssetBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=64)
    type: AssetType
    value: Decimal


class Asset(AssetBase):
    id: int


class GetAssetsResponse(BaseSchema):
    assets: list[Asset]


class PostAssetRequest(AssetBase):
    pass


class UpdateAssetRequest(AssetBase):
    pass
