import logging

try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except (ImportError, ModuleNotFoundError):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)

from routing.intent_classifier import IntentClassifier


class QueryRouter:
    def __init__(
        self,
        rag_pipeline,
        kag_pipeline,
        response_generator,
        semantic_cache
    ):
        logger.info(f'Observability: {__name__}.__init__ was called')
        print(f'DEBUG: Executing {__name__}.__init__')

        self.semantic_cache = semantic_cache   # 🔥 Hybrid cache
        self.classifier = IntentClassifier()

        self.rag_pipeline = rag_pipeline
        self.kag_pipeline = kag_pipeline
        self.response_generator = response_generator

    def route(self, query: str):

        logger.info(f'Observability: {__name__}.route was called')
        print(f'DEBUG: Executing {__name__}.route')

        # 🔹 1. Intent FIRST (CRITICAL FIX)
        intent = self.classifier.classify(query)

        # 🔹 2. Cache ONLY for RAG
        if intent == "RAG":
            cached_response = self.semantic_cache.search(query)

            if cached_response:
                print("⚡ Cache HIT (Hybrid)")
                return {
                    "source": "CAG",
                    "response": cached_response
                }

        # 🔹 3. Routing
        if intent == "KAG":
            response = self._handle_kag(query)

        elif intent == "RAG":
            response = self._handle_rag(query)

        else:
            response = self._handle_hybrid(query)

        # 🔹 4. Store ONLY RAG responses
        if intent == "RAG":
            # Ensure response is a string before caching (fixes AIMessage JSON serialization error)
            response_str = response.content if hasattr(response, "content") else str(response)
            self.semantic_cache.add(query, response_str)

        return {
            "source": intent,
            "response": response.content if hasattr(response, "content") else response
        }

    # -----------------------------
    # 🔹 RAG
    # -----------------------------
    def _handle_rag(self, query):
        logger.info(f'Observability: {__name__}._handle_rag was called')
        print(f'DEBUG: Executing {__name__}._handle_rag')

        docs = self.rag_pipeline.retrieve(query)
        context = "\n".join([doc.page_content for doc in docs])

        return self.response_generator.generate(query, context)

    # -----------------------------
    # 🔹 KAG (with fallback)
    # -----------------------------
    def _handle_kag(self, query):
        logger.info(f'Observability: {__name__}._handle_kag was called')
        print(f'DEBUG: Executing {__name__}._handle_kag')

        try:
            context = self.kag_pipeline.retrieve(query)
            return self.response_generator.generate(query, context)

        except Exception as e:
            logger.error(f"KAG failed: {e}")
            print("⚠️ Falling back to RAG")
            return self._handle_rag(query)

    # -----------------------------
    # 🔹 HYBRID (RAG + KAG)
    # -----------------------------
    def _handle_hybrid(self, query):
        logger.info(f'Observability: {__name__}._handle_hybrid was called')
        print(f'DEBUG: Executing {__name__}._handle_hybrid')

        try:
            # RAG
            rag_docs = self.rag_pipeline.retrieve(query)
            rag_context = "\n".join([doc.page_content for doc in rag_docs])

            # KAG
            kag_context = self.kag_pipeline.retrieve(query)

            combined_context = f"""
            RAG Context:
            {rag_context}

            KAG Context:
            {kag_context}
            """

            return self.response_generator.generate(query, combined_context)

        except Exception as e:
            logger.error(f"Hybrid failed: {e}")
            print("⚠️ Hybrid fallback to RAG")
            return self._handle_rag(query)