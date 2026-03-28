import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
class RAGPipeline:
    def __init__(self, vectordb):
        logger.info(f'Observability: {__name__}.__init__ was called')
        print(f'DEBUG: Executing {__name__}.__init__')
        self.vectordb = vectordb

    def retrieve(self, query):
        logger.info(f'Observability: {__name__}.retrieve was called')
        print(f'DEBUG: Executing {__name__}.retrieve')
        return self.vectordb.query(query)