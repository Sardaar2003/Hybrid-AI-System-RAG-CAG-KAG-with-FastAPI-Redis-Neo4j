import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from langchain_community.vectorstores import FAISS


class SemanticCache:
    def __init__(self, embedding_model):
        logger.info(f'Observability: {__name__}.__init__ was called')
        print(f'DEBUG: Executing {__name__}.__init__')
        self.embedding_model = embedding_model
        self.cache_store = None

    def add(self, query: str, response: str):
        logger.info(f'Observability: {__name__}.add was called')
        print(f'DEBUG: Executing {__name__}.add')
        texts = [query]
        metadatas = [{"response": response}]

        if self.cache_store is None:
            self.cache_store = FAISS.from_texts(
                texts,
                self.embedding_model,
                metadatas=metadatas
            )
        else:
            self.cache_store.add_texts(
                texts,
                metadatas=metadatas
            )

    def search(self, query: str, threshold=0.85):
        logger.info(f'Observability: {__name__}.search was called')
        print(f'DEBUG: Executing {__name__}.search')
        if self.cache_store is None:
            return None

        results = self.cache_store.similarity_search_with_score(query, k=1)

        if not results:
            return None

        doc, score = results[0]

        # FAISS returns distance → convert to similarity
        similarity = 1 - score

        if similarity >= threshold:
            return doc.metadata["response"]

        return None