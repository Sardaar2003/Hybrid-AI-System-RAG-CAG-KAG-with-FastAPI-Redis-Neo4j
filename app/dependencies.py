import logging

try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)

# 🔹 Core imports
from embeddings.embedder import get_embedding_model
from vectorstore.vectordb import VectorDB

# 🔥 CHANGE HERE (IMPORTANT)
from cache.hybrid_cache import HybridCache

from orchestration.response_generator import ResponseGenerator
from knowledge_graph.neo4j_store import Neo4jStore
from retrieval.rag_pipeline import RAGPipeline
from knowledge_graph.graph_retriever import KAGPipeline
from routing.query_router import QueryRouter


def get_system():
    logger.info(f'Observability: {__name__}.get_system was called')
    print(f'DEBUG: Executing {__name__}.get_system')

    # -----------------------------
    # 🔹 Embedding Model
    # -----------------------------
    embedding_model = get_embedding_model()

    # -----------------------------
    # 🔹 Vector DB (RAG)
    # -----------------------------
    vectordb = VectorDB(embedding_model)
    vectordb.load()

    # -----------------------------
    # 🔥 Hybrid Cache (Redis + Semantic)
    # -----------------------------
    cache = HybridCache(embedding_model)

    # -----------------------------
    # 🔹 Knowledge Graph (KAG)
    # -----------------------------
    neo4j_store = Neo4jStore()

    # -----------------------------
    # 🔹 Pipelines
    # -----------------------------
    rag_pipeline = RAGPipeline(vectordb)
    kag_pipeline = KAGPipeline(neo4j_store)

    # -----------------------------
    # 🔹 LLM
    # -----------------------------
    response_generator = ResponseGenerator()

    # -----------------------------
    # 🔹 Router (Brain)
    # -----------------------------
    router = QueryRouter(
        rag_pipeline=rag_pipeline,
        kag_pipeline=kag_pipeline,
        response_generator=response_generator,
        semantic_cache=cache   # 🔥 Hybrid cache injected
    )

    return router