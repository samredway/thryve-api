from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from app.schemas.base import BaseSchema


class AssetType(StrEnum):
    crypto = "crypto"
    stocks = "stocks"
    property = "property"
    cash = "cash"
    other = "other"


class Asset(BaseSchema):
    id: int
    name: str = Field(..., min_length=1, max_length=64)
    type: AssetType
    value: Decimal = Field(..., gt=0)


class GetAssetsResponse(BaseSchema):
    assets: list[Asset]


class PostAssetRequest(BaseSchema):
    type: str
    name: str
    value: Decimal


class UpdateAssetRequest(PostAssetRequest):
    pass
