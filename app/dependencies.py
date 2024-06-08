from typing import AsyncGenerator, Any, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal


async def get_session() -> AsyncGenerator[Session, Any]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


SessionDependency = Annotated[Session, Depends(get_session)]
