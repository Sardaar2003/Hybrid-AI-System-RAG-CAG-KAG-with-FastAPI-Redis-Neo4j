import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from fastapi import APIRouter
from pydantic import BaseModel

from app.dependencies import get_system

router = APIRouter()

# ✅ Get full system (includes semantic cache)
query_router = get_system()


class QueryRequest(BaseModel):
    query: str


@router.post("/")
def query_system(request: QueryRequest):
    logger.info(f'Observability: {__name__}.query_system was called')
    print(f'DEBUG: Executing {__name__}.query_system')
    result = query_router.route(request.query)

    return {
        "query": request.query,
        "source": result["source"],
        "response": result["response"]
    }