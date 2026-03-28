import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from langchain_community.vectorstores import FAISS
import os


class VectorDB:
    def __init__(self, embedding_model, path="vector_db"):
        logger.info(f'Observability: {__name__}.__init__ was called')
        print(f'DEBUG: Executing {__name__}.__init__')
        self.embedding_model = embedding_model
        self.path = path
        self.db = None

    def build(self, documents, batch_size=50):
        logger.info(f'Observability: {__name__}.build was called')
        print(f'DEBUG: Executing {__name__}.build')
        from tqdm import tqdm
        
        self.db = None
        for i in tqdm(range(0, len(documents), batch_size), desc="Building FAISS Index"):
            batch = documents[i:i+batch_size]
            if self.db is None:
                self.db = FAISS.from_documents(batch, self.embedding_model)
            else:
                self.db.add_documents(batch)
                
        if self.db is not None:
            self.db.save_local(self.path)

    def load(self):
        logger.info(f'Observability: {__name__}.load was called')
        print(f'DEBUG: Executing {__name__}.load')
        if os.path.exists(self.path):
            self.db = FAISS.load_local(
                self.path,
                self.embedding_model,
                allow_dangerous_deserialization=True
            )

    def query(self, query, k=3):
        logger.info(f'Observability: {__name__}.query was called')
        print(f'DEBUG: Executing {__name__}.query')
        return self.db.similarity_search(query, k=k)