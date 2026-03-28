import logging
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
from langchain_openai import ChatOpenAI
from config.settings import settings


class ResponseGenerator:
    def __init__(self):
        logger.info(f'Observability: {__name__}.__init__ was called')
        print(f'DEBUG: Executing {__name__}.__init__')
        self.llm = ChatOpenAI(
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )

    def generate(self, query, context):
        logger.info(f'Observability: {__name__}.generate was called')
        print(f'DEBUG: Executing {__name__}.generate')
        prompt = f"""
        Answer the question based on the context.

        Context:
        {context}

        Question:
        {query}
        """
        return self.llm.invoke(prompt)