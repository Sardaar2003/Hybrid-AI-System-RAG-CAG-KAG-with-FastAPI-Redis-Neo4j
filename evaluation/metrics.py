import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
import time


def measure_latency(func, *args, **kwargs):
    logger.info(f'Observability: {__name__}.measure_latency was called')
    print(f'DEBUG: Executing {__name__}.measure_latency')
    start = time.time()
    result = func(*args, **kwargs)
    latency = time.time() - start
    return result, latency


def simple_accuracy(prediction: str, ground_truth: str):
    logger.info(f'Observability: {__name__}.simple_accuracy was called')
    print(f'DEBUG: Executing {__name__}.simple_accuracy')
    return int(ground_truth.lower() in prediction.lower())


def hallucination_score(prediction: str, context: str):
    """
    Basic heuristic:
    If answer contains info NOT in context → hallucination risk
    """
    logger.info(f'Observability: {__name__}.hallucination_score was called')
    print(f'DEBUG: Executing {__name__}.hallucination_score')
    return int(prediction not in context)