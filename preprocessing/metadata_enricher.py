import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from tqdm import tqdm

def enrich_metadata(documents):
    logger.info(f'Observability: {__name__}.enrich_metadata was called')
    print(f'DEBUG: Executing {__name__}.enrich_metadata')
    for doc in tqdm(documents, desc="Enriching metadata"):
        doc.metadata["length"] = len(doc.page_content)
    return documents