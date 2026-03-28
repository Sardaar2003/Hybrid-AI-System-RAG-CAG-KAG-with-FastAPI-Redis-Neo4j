import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path: str):
    logger.info(f'Observability: {__name__}.load_pdf was called')
    print(f'DEBUG: Executing {__name__}.load_pdf')
    loader = PyPDFLoader(file_path)
    return loader.load()