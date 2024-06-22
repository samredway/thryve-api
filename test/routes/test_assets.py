from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.asset import Asset


def test_get_assets(client: TestClient, asset: Asset) -> None:
    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json().get("assets") is not None
    assert response.json().get("assets")[0].get("name") == asset.name


def test_post_asset(client: TestClient, session: Session) -> None:
    name = str(uuid4())
    response = client.post("/assets", json={"type": "test", "name": name, "value": 200})
    assert response.status_code == 200, response.text
    assert response.json().get("name") == name

    stmt = select(Asset).where(Asset.name == name)
    test_asset = session.execute(stmt).scalars().one()
    assert test_asset


def test_update_asset(client: TestClient, asset: Asset) -> None:
    new_name = str(uuid4())
    response = client.put(
        f"/assets/{asset.id}", json={"type": "test", "name": new_name, "value": 200}
    )
    assert response.status_code == 200, response.text
    assert response.json().get("name") == new_name
