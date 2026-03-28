test_queries = [
    {
        "query": "What is the revenue of Tesla?",
        "type": "RAG",
        "ground_truth": "Tesla revenue is ..."
    },
    {
        "query": "Who works at prismaticAI?",
        "type": "KAG",
        "ground_truth": "Sarah and Michael work at prismaticAI"
    },
    {
        "query": "Explain AI briefly",
        "type": "CAG",
        "ground_truth": "AI is ..."
    },
    {
        "query": "Does Sarah work with Michael?",
        "type": "KAG",
        "ground_truth": "Yes, both work at the same company"
    }
]