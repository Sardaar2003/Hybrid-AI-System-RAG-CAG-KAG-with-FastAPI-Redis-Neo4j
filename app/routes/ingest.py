import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from fastapi import APIRouter, UploadFile, File
import shutil
import os

from ingestion.ingestion_pipeline import ingest_data
from preprocessing.chunker import chunk_documents
from preprocessing.metadata_enricher import enrich_metadata
from embeddings.embedder import get_embedding_model
from vectorstore.vectordb import VectorDB
from knowledge_graph.graph_builder import GraphBuilder
from knowledge_graph.neo4j_store import Neo4jStore

router = APIRouter()

UPLOAD_DIR = "data/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

embedding_model = get_embedding_model()
vectordb = VectorDB(embedding_model)
graph_builder = GraphBuilder()
neo4j_store = Neo4jStore()


@router.post("/")
async def ingest(file: UploadFile = File(...)):
    logger.info(f'Observability: {__name__}.ingest was called')
    print(f'DEBUG: Executing {__name__}.ingest')
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1. Load
    docs = ingest_data(file_path)

    # 2. Chunk
    chunks = chunk_documents(docs)

    # 3. Metadata
    chunks = enrich_metadata(chunks)

    # 4. Vector DB
    vectordb.build(chunks)

    # 5. Knowledge Graph
    graph_docs = graph_builder.build_graph(chunks)
    
    # 6. Save Knowledge Graph to Neo4j database
    neo4j_store.save_graph_documents(graph_docs)

    return {
        "message": "Ingestion successful",
        "chunks": len(chunks),
        "graph_docs": len(graph_docs)
    }