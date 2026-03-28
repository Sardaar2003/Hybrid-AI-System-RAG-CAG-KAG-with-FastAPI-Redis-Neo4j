import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from langchain_openai import OpenAIEmbeddings
from config.settings import settings


def get_embedding_model():
    logger.info(f'Observability: {__name__}.get_embedding_model was called')
    print(f'DEBUG: Executing {__name__}.get_embedding_model')
    return OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY
    )