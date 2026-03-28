# Enterprise AI System: Hybrid RAG, KAG & CAG
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Neo4j](https://img.shields.io/badge/Neo4j-018bff?style=for-the-badge&logo=neo4j&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

A modular, enterprise-grade AI pipeline built to dynamically route user queries across three powerful retrieval strategies:
1. **RAG (Retrieval-Augmented Generation)**: Uses dense vector embeddings and a Vector DB to retrieve similarity-based factual context.
2. **KAG (Knowledge-Augmented Generation)**: Leverages OpenAI's LLM Graph Transformer to extract entity relationships and stores them in Neo4j for semantic relationship queries.
3. **CAG (Cache-Augmented Generation)**: A sub-millisecond layer relying on Redis and Semantic Caching to intercept repetitive queries, skipping LLM costs entirely.

## 🚀 Features
- **Dynamic Intent Routing**: The system runs queries against a lightweight classifier to accurately determine whether a question asks for factual data (RAG) or entity connections (KAG).
- **Premium Frontend Dashboard**: A glassmorphism-styled UI built in pure Vanilla JS/HTML/CSS, served natively via FastAPI `StaticFiles`.
- **Automated Graph Ingestion**: Drop a CSV, PDF, or TXT into the UI to automatically chunk the document, build the vector embeddings, extract graph relationships, and save them to Neo4j.
- **Micro-Animations & Visual Pipeline**: Watch the UI glow dynamically with custom badges defining exactly which subsystem (RAG/KAG/Hybrid) fielded the request.

## 🛠️ Architecture
The system consists of the following components:
* `FastAPI`: The core asynchronous backend mapping REST endpoints.
* `LangChain`: Core logic for `LLMGraphTransformer`, embeddings, and response orchestration.
* `Neo4j Aura`: Cloud graph database executing cypher queries to trace relationships.
* `Vector DB`: Retrieves context based on cosine similarity of text embeddings.
* `Redis`: Lightning-fast, exact-match string caching layer.

## ⚙️ Local Setup

### 1. Requirements
Ensure you have Python 3.9+ and a local or cloud Neo4j and Redis instance accessible.

### 2. Installation
```bash
git clone https://github.com/Sardaar2003/Hybrid-AI-System-RAG-CAG-KAG-with-FastAPI-Redis-Neo4j.git
cd Hybrid-AI-System-RAG-CAG-KAG-with-FastAPI-Redis-Neo4j/enterprise_ai_system

python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and populate it with your keys:
```env
OPENAI_API_KEY=sk-...
NEO4J_URI=neo4j+s://<YOUR_AURA_ID>.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=<YOUR_PASSWORD>
NEO4J_DATABASE=<YOUR_DATABASE_NAME> # Defaults to neo4j
REDIS_URL=redis://localhost:6379
```

### 4. Running the Server
```bash
uvicorn app.main:app --reload
```
Once Uvicorn starts, navigate locally to **[http://127.0.0.1:8000](http://127.0.0.1:8000)** to view the AI Dashboard.

## 🧪 Testing the Pipelines
Try typing these queries into the Dashboard to test the intelligent routing:

* **RAG Trigger**: *"What are the steps to reset a forgotten PIN?"*
* **CAG Trigger**: Quickly ask the exact same question. The answer will load instantaneously from the Redis Semantic Cache!
* **KAG Trigger**: *"What is the relationship between a mobile device and company email?"* (The classifier detects relationship keywords and fires graph cypher queries!)

---
*Developed for the RAG/KAG/CAG Enterprise AI System Project.*
