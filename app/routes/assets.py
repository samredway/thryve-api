from fastapi import APIRouter

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

router = APIRouter(prefix="/assets", tags=["Auth"])


@router.get("/")
def get_assets(
    cognito_id: AuthorizedUserDependency, session: SessionDependency
) -> GetAssetsResponse:
    stmt = get_user_by_cognito_id(cognito_id=cognito_id)
    user: User = session.execute(stmt).scalars().one()
    return GetAssetsResponse(
        assets=[Asset.model_validate(asset) for asset in user.assets]
    )


@router.post("/")
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


@router.put("/{asset_id}")
def update_asset(
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
