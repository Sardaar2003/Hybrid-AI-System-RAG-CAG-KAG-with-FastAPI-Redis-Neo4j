from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

from app.routes.query import router as query_router
from app.routes.health import router as health_router
from app.routes.ingest import router as ingest_router


app = FastAPI(title="Enterprise AI System (RAG + CAG + KAG)")

# Mount routes
app.include_router(ingest_router, prefix="/ingest")
app.include_router(query_router, prefix="/query")
app.include_router(health_router, prefix="/health")

# Determine paths dynamically for serving static files
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Ensure frontend dir exists to avoid crash on startup
if not FRONTEND_DIR.exists():
    FRONTEND_DIR.mkdir()

# Mount frontend
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Redirect root to the premium frontend"""
    return RedirectResponse(url="/static/index.html")