import redis
import json
import logging

try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)


class RedisCache:
    def __init__(self):
        try:
            self.client = redis.Redis(
                host="localhost",
                port=6379,   # change if using 6380
                decode_responses=True,
                socket_connect_timeout=2,  # Fail fast if Redis is down
                socket_timeout=2
            )
        except Exception as e:
            logger.error(f"Failed to initialize Redis client: {e}")
            self.client = None

    def _normalize_key(self, query: str) -> str:
        """Normalize the query string to prevent trivial cache misses."""
        return query.strip().lower()

    def add(self, query: str, response: str, ttl_seconds: int = 3600):
        if not self.client:
            return
            
        try:
            key = self._normalize_key(query)
            # Add entry with expiration (TTL)
            self.client.set(key, json.dumps({"response": response}), ex=ttl_seconds)
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis cache Add error: {e}")

    def search(self, query: str):
        if not self.client:
            return None
            
        try:
            key = self._normalize_key(query)
            result = self.client.get(key)

            if result:
                return json.loads(result)["response"]
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis cache Search error: {e}")
            
        return None