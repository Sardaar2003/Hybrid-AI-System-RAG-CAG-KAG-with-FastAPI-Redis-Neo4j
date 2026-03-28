import logging

try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)


class KAGPipeline:
    def __init__(self, graph_store):
        logger.info(f'Observability: {__name__}.__init__ was called')
        print(f'DEBUG: Executing {__name__}.__init__')
        self.graph_store = graph_store

    def retrieve(self, query: str):

        logger.info(f'Observability: {__name__}.retrieve was called')
        print(f'DEBUG: Executing {__name__}.retrieve')

        # 🔹 1. Extract keywords
        keywords = query.lower().split()

        # 🔹 2. Cypher query
        cypher_query = """
        MATCH (n)-[r]->(m)
        WHERE ANY(k IN $keywords 
            WHERE toLower(n.id) CONTAINS k 
            OR toLower(m.id) CONTAINS k)
        RETURN n.id AS n, type(r) AS r, m.id AS m
        LIMIT 20
        """

        try:
            # 🔹 3. Execute query (now returns LIST)
            results = self.graph_store.run_query(
                cypher_query,
                {"keywords": keywords}
            )

            # 🔹 4. Build context safely
            context = ""

            for record in results:
                try:
                    n = record.get("n", {})
                    r = record.get("r", {})
                    m = record.get("m", {})

                    context += f"{n} -[{r}]-> {m}\n"

                except Exception as e:
                    logger.warning(f"Error parsing record: {e}")

            # 🔹 5. Fallback if empty
            if not context:
                context = "No relationships found in knowledge graph."

            return context

        except Exception as e:
            logger.error(f"KAG retrieval failed: {e}")
            return "Knowledge graph retrieval failed."