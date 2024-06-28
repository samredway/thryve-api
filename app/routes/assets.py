from fastapi import APIRouter, HTTPException

from app.dependencies import AuthorizedUserDependency, SessionDependency
from app.schemas.assets import (
    GetAssetsResponse,
    Asset,
    PostAssetRequest,
    UpdateAssetRequest,
)
from app.models.user import User
from app.repositories.asset import create_asset, select_asset_for_update
from app.repositories.user import get_user_by_cognito_id

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/assets")
def get_assets(
    cognito_id: AuthorizedUserDependency, session: SessionDependency
) -> GetAssetsResponse:
    stmt = get_user_by_cognito_id(cognito_id=cognito_id)
    user: User = session.execute(stmt).scalars().one()
    return GetAssetsResponse(
        assets=[Asset.model_validate(asset) for asset in user.assets]
    )


@router.post("/asset")
def post_asset(
    cognito_id: AuthorizedUserDependency,
    session: SessionDependency,
    request: PostAssetRequest,
) -> Asset:
    stmt = get_user_by_cognito_id(cognito_id=cognito_id)
    user = session.execute(stmt).scalar_one()
    asset = create_asset(
        user_id=user.id,
        type=request.type,
        name=request.name,
        value=request.value,
    )
    session.add(asset)
    session.commit()
    return Asset.model_validate(asset)


@router.delete("/asset/{asset_id}")
def delete_asset(
    cognito_id: AuthorizedUserDependency,
    session: SessionDependency,
    asset_id: int,
) -> None:
    stmt = select_asset_for_update(asset_id=asset_id)
    asset = session.execute(stmt).scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    session.delete(asset)
    session.commit()


@router.put("/asset/{asset_id}")
def update_asset(
    cognito_id: AuthorizedUserDependency,
    request: UpdateAssetRequest,
    session: SessionDependency,
    asset_id: int,
) -> Asset:
    stmt = select_asset_for_update(asset_id=asset_id)
    asset = session.execute(stmt).scalar_one()
    asset.name = request.name
    asset.value = request.value
    asset.type = request.type
    session.commit()
    return Asset.model_validate(asset)
