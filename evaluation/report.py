import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
def summarize(results):
    logger.info(f'Observability: {__name__}.summarize was called')
    print(f'DEBUG: Executing {__name__}.summarize')
    summary = {}

    for r in results:
        src = r["source"]

        if src not in summary:
            summary[src] = {
                "count": 0,
                "accuracy": 0,
                "latency": 0
            }

        summary[src]["count"] += 1
        summary[src]["accuracy"] += r["accuracy"]
        summary[src]["latency"] += r["latency"]

    for src in summary:
        summary[src]["accuracy"] /= summary[src]["count"]
        summary[src]["latency"] /= summary[src]["count"]

    return summary