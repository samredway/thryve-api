from decimal import Decimal

from app.schemas.base import BaseSchema


class Asset(BaseSchema):
    id: int
    name: str
    type: str
    value: Decimal


class GetAssetsResponse(BaseSchema):
    assets: list[Asset]


class PostAssetRequest(BaseSchema):
    type: str
    name: str
    value: Decimal


class UpdateAssetRequest(PostAssetRequest):
    pass
