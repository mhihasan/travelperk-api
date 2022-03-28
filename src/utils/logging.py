import logging

from src.core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)
