import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from evaluation.evaluator import Evaluator
from evaluation.test_dataset import test_queries
from app.dependencies import get_system


def run_evaluation():
    logger.info(f'Observability: {__name__}.run_evaluation was called')
    print(f'DEBUG: Executing {__name__}.run_evaluation')
    router = get_system()

    evaluator = Evaluator(router)
    results = evaluator.evaluate(test_queries)

    print(results)


if __name__ == "__main__":
    run_evaluation()