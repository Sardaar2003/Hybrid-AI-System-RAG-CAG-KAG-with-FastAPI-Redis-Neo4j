import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from neo4j import GraphDatabase
from config.settings import settings
from langchain_neo4j import Neo4jGraph

class Neo4jStore:
    def __init__(self):
        logger.info(f'Observability: {__name__}.__init__ was called')
        print(f'DEBUG: Executing {__name__}.__init__')
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        try:
            self.graph = Neo4jGraph(
                url=settings.NEO4J_URI,
                username=settings.NEO4J_USER,
                password=settings.NEO4J_PASSWORD,
                database=settings.NEO4J_DATABASE
            )
        except Exception as e:
            logger.error(f"Failed to initialize Neo4jGraph (LangChain): {e}")
            self.graph = None

    def close(self):
        logger.info(f'Observability: {__name__}.close was called')
        print(f'DEBUG: Executing {__name__}.close')
        self.driver.close()

    def run_query(self, query, params=None):
        logger.info(f'Observability: {__name__}.run_query was called')
        print(f'DEBUG: Executing {__name__}.run_query')
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return list(result)   # ✅ IMPORTANT FIX
            
    def save_graph_documents(self, graph_docs):
        logger.info(f'Observability: {__name__}.save_graph_documents was called')
        print(f'DEBUG: Executing {__name__}.save_graph_documents')
        if not self.graph:
            logger.error("Neo4jGraph is not initialized. Cannot save documents.")
            return False
            
        if not graph_docs:
            logger.warning("No graph documents to save.")
            return True
            
        try:
            # Langchain's built-in way to securely merge GraphDocuments to Neo4j
            self.graph.add_graph_documents(graph_docs, baseEntityLabel=True, include_source=True)
            logger.info(f"Successfully saved {len(graph_docs)} graph documents to Neo4j.")
            return True
        except Exception as e:
            logger.error(f"Failed to save graph documents: {e}")
            return False