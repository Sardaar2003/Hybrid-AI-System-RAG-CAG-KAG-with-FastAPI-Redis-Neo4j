import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
import redis
from config.settings import settings


class CacheManager:
    def __init__(self):
        logger.info(f'Observability: {__name__}.__init__ was called')
        print(f'DEBUG: Executing {__name__}.__init__')
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

    def get(self, key: str):
        logger.info(f'Observability: {__name__}.get was called')
        print(f'DEBUG: Executing {__name__}.get')
        return self.client.get(key)

    def set(self, key: str, value: str):
        logger.info(f'Observability: {__name__}.set was called')
        print(f'DEBUG: Executing {__name__}.set')
        self.client.set(key, value)