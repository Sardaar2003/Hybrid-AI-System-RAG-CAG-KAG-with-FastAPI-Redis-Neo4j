import logging
from cache.semantic_cache import SemanticCache
from cache.redis_cache import RedisCache

try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)


class HybridCache:
    def __init__(self, embedding_model):
        self.redis_cache = RedisCache()
        self.semantic_cache = SemanticCache(embedding_model)

    def search(self, query: str):

        # 🔹 1. Redis (exact match)
        try:
            redis_result = self.redis_cache.search(query)
            if redis_result:
                print("⚡ Redis Cache HIT")
                return redis_result
        except Exception as e:
            logger.error(f"Error accessing Redis cache in hybrid search: {e}")

        # 🔹 2. Semantic (FAISS)
        try:
            semantic_result = self.semantic_cache.search(query)
            if semantic_result:
                print("🧠 Semantic Cache HIT")
                return semantic_result
        except Exception as e:
            logger.error(f"Error accessing Semantic cache in hybrid search: {e}")

        print("❌ Cache MISS")
        return None

    def add(self, query: str, response: str):

        # 🔹 Store in both caches (with independent error handling)
        try:
            self.redis_cache.add(query, response)
        except Exception as e:
            logger.error(f"Failed to add to Redis cache in hybrid add: {e}")
            
        try:
            self.semantic_cache.add(query, response)
        except Exception as e:
            logger.error(f"Failed to add to Semantic cache in hybrid add: {e}")