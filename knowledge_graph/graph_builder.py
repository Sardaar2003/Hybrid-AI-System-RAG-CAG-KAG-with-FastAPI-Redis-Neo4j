import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from config.settings import settings


class GraphBuilder:
    def __init__(self):
        logger.info(f'Observability: {__name__}.__init__ was called')
        print(f'DEBUG: Executing {__name__}.__init__')
        self.llm = ChatOpenAI(
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.transformer = LLMGraphTransformer(llm=self.llm)

    def build_graph(self, documents, batch_size=10):
        logger.info(f'Observability: {__name__}.build_graph was called')
        print(f'DEBUG: Executing {__name__}.build_graph')
        from tqdm import tqdm
        
        graph_documents = []
        for i in tqdm(range(0, len(documents), batch_size), desc="Extracting Knowledge Graph"):
            batch = documents[i:i+batch_size]
            batch_graphs = self.transformer.convert_to_graph_documents(batch)
            graph_documents.extend(batch_graphs)
            
        return graph_documents