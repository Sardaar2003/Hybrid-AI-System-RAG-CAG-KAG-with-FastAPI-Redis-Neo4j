import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from ingestion.loaders.pdf_loader import load_pdf
from ingestion.loaders.txt_loader import load_txt
from ingestion.loaders.csv_loader import load_csv


def ingest_data(file_path: str):
    logger.info(f'Observability: {__name__}.ingest_data was called')
    print(f'DEBUG: Executing {__name__}.ingest_data')
    if file_path.endswith(".pdf"):
        return load_pdf(file_path)
    elif file_path.endswith(".txt"):
        return load_txt(file_path)
    elif file_path.endswith(".csv"):
        return load_csv(file_path)
    else:
        raise ValueError("Unsupported file format")