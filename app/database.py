import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.exceptions import ConfigurationError

env = os.getenv("ENV")
db_user = os.getenv("DB_USER", "")
db_pass = os.getenv("DB_PASS", "")
db_url = os.getenv("DB_URL")

if not db_user and db_pass and db_url:
    raise ConfigurationError("DB not correctly configured. Missing credentials")

db_string = f"postgresql://{db_user}:{db_pass}@{db_url}/thryve_api_db"

engine = create_engine(db_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
