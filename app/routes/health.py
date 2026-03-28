import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    logger.info(f'Observability: {__name__}.health_check was called')
    print(f'DEBUG: Executing {__name__}.health_check')
    return {"status": "ok"}