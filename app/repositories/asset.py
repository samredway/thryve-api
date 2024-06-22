from decimal import Decimal

from sqlalchemy import Select, select

from app.models.asset import Asset


def create_asset(*, user_id: int, type: str, name: str, value: Decimal) -> Asset:
    new_asset: Asset = Asset(
        user_id=user_id,
        type=type,
        name=name,
        value=value,
    )
    return new_asset


def select_asset_for_update(asset_id: int) -> Select[tuple[Asset]]:
    stmt = select(Asset).where(Asset.id == asset_id).with_for_update()
    return stmt
