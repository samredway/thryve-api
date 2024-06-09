import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.exceptions import ConfigurationError

SQLALCHEMY_DATABASE_URL = os.getenv("DB_STRING", '')

if not SQLALCHEMY_DATABASE_URL:
    raise ConfigurationError("No DB_STRING provided")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
