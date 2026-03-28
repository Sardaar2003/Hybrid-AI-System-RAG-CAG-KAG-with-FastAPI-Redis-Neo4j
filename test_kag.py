import os
import sys

from app.dependencies import get_system
from ingestion.ingestion_pipeline import ingest_data
from preprocessing.chunker import chunk_documents
from preprocessing.metadata_enricher import enrich_metadata
from embeddings.embedder import get_embedding_model
from vectorstore.vectordb import VectorDB
from knowledge_graph.graph_builder import GraphBuilder
from knowledge_graph.neo4j_store import Neo4jStore

def run_test():
    print("Initializing components...")
    router = get_system()
    embedding_model = get_embedding_model()
    vectordb = VectorDB(embedding_model)
    graph_builder = GraphBuilder()
    neo4j_store = Neo4jStore()

    file_path = r"C:\Users\singh\OneDrive\Desktop\GENAI_Course\RAG_KAG_Project\enterprise_ai_system\rag_sample_qas_from_kis.csv"

    print(f"\n[1/6] Loading data from {file_path}...")
    docs = ingest_data(file_path)
    
    # 🔹 Slice down to 2 docs to speed up graph testing
    docs = docs[:2]
    print(f"Loaded {len(docs)} documents from CSV snippet for test.")

    print("\n[2/6] Chunking Documents...")
    chunks = chunk_documents(docs)
    print(f"Generated {len(chunks)} chunks.")

    print("\n[3/6] Enriching Metadata...")
    chunks = enrich_metadata(chunks)

    print("\n[4/6] Building VectorDB (for completeness)...")
    vectordb.build(chunks)

    print("\n[5/6] Extracting Knowledge Graph via LLM...")
    graph_docs = graph_builder.build_graph(chunks)
    print(f"Extracted {len(graph_docs)} graph documents.")

    print("\n[6/6] Saving Knowledge Graph to Neo4j...")
    success = neo4j_store.save_graph_documents(graph_docs)
    print(f"Save Success: {success}")

    print("\n--- INGESTION COMPLETE ---\n")

    print("\n--- KAG PIPELINE TEST ---\n")
    test_query = "How do I set up my company email on my mobile device?"
    print(f"Test Query: '{test_query}'\n")

    print("[Step 1] Retrieving Graph Context (KAG)...")
    context = router.kag_pipeline.retrieve(test_query)
    print("\n--- Retrieved Graph Context ---")
    print(context)
    print("-------------------------------\n")

    print("[Step 2] Generating LLM Response using KAG Context...")
    response = router.response_generator.generate(test_query, context)
    
    # Extract string nicely
    response_text = response.content if hasattr(response, "content") else str(response)
    
    print("\n--- Final KAG Response ---")
    print(response_text)
    print("--------------------------\n")
    
    print("Test finished successfully!")

if __name__ == "__main__":
    run_test()
