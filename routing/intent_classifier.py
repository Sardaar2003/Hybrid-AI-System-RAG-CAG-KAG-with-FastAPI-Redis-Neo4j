import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
class IntentClassifier:

    RELATIONSHIP_KEYWORDS = [
        "relationship",
        "related",
        "connected",
        "between",
        "who works with",
        "same company",
        "depends on"
    ]

    def classify(self, query: str) -> str:
        logger.info(f'Observability: {__name__}.classify was called')
        print(f'DEBUG: Executing {__name__}.classify')
        query_lower = query.lower()

        for keyword in self.RELATIONSHIP_KEYWORDS:
            if keyword in query_lower:
                return "KAG"

        if query_lower.startswith(("what", "when", "where", "define", "explain")):
            return "RAG"

        return "HYBRID"