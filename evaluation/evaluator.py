import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from evaluation.metrics import measure_latency, simple_accuracy


class Evaluator:
    def __init__(self, router):
        logger.info(f'Observability: {__name__}.__init__ was called')
        print(f'DEBUG: Executing {__name__}.__init__')
        self.router = router

    def evaluate(self, dataset):
        logger.info(f'Observability: {__name__}.evaluate was called')
        print(f'DEBUG: Executing {__name__}.evaluate')
        from tqdm import tqdm
        results = []

        for item in tqdm(dataset, desc="Evaluating Dataset RAG/CAG/KAG responses"):
            query = item["query"]
            ground_truth = item["ground_truth"]

            response_data, latency = measure_latency(
                self.router.route,
                query
            )

            prediction = response_data["response"]

            accuracy = simple_accuracy(prediction, ground_truth)

            results.append({
                "query": query,
                "source": response_data["source"],
                "latency": latency,
                "accuracy": accuracy
            })

        return results