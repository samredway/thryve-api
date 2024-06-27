from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.asset import Asset


def test_get_assets(client: TestClient, asset: Asset) -> None:
    response = client.get("/assets/assets")
    assert response.status_code == 200
    assert response.json().get("assets") is not None
    assert response.json().get("assets")[0].get("name") == asset.name


def test_post_asset(client: TestClient, session: Session) -> None:
    name = str(uuid4())
    response = client.post(
        "/assets/asset", json={"type": "test", "name": name, "value": 200}
    )
    assert response.status_code == 200, response.text
    assert response.json().get("name") == name

    stmt = select(Asset).where(Asset.name == name)
    test_asset = session.execute(stmt).scalars().one()
    assert test_asset


def test_update_asset(client: TestClient, asset: Asset) -> None:
    new_name = str(uuid4())
    response = client.put(
        f"/assets/asset/{asset.id}",
        json={"type": "test", "name": new_name, "value": 200},
    )
    assert response.status_code == 200, response.text
    assert response.json().get("name") == new_name


def test_delete_asset(client: TestClient, asset: Asset, session: Session) -> None:
    response = client.delete(f"/assets/asset/{asset.id}")
    assert response.status_code == 200, response.text

    stmt = select(Asset).where(Asset.id == asset.id)
    test_asset = session.execute(stmt).scalars().first()
    assert test_asset is None


def test_delete_asset_not_found(client: TestClient, asset: Asset) -> None:
    response = client.delete(f"/assets/asset/{asset.id + 10}")
    assert response.status_code == 404
    assert response.json().get("detail") == "Asset not found"
