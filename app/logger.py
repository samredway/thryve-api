import os
import logging
from logging import getLogger

env = os.environ.get("ENV", "prod")

logger = getLogger("uvicorn.error")

if env == "local":
    logger.setLevel(logging.DEBUG)
