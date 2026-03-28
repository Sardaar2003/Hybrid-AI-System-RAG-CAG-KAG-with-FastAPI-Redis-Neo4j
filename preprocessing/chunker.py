import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm


def chunk_documents(documents):
    logger.info(f'Observability: {__name__}.chunk_documents was called')
    print(f'DEBUG: Executing {__name__}.chunk_documents')
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    # Wrap in list so it consumes the tqdm iterator immediately and shows progress
    return splitter.split_documents(tqdm(documents, desc="Chunking documents"))