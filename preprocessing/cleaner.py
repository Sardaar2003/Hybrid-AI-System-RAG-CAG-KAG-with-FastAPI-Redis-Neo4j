import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
def clean_text(text: str) -> str:
    logger.info(f'Observability: {__name__}.clean_text was called')
    print(f'DEBUG: Executing {__name__}.clean_text')
    return text.strip().replace("\n", " ")