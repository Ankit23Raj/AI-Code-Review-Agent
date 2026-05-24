import math

from app.rag.embeddings import create_embeddings
from app.rag.indexer import INDEX


def cosine_similarity(vec1, vec2):
    if not vec1 or not vec2:
        return 0.0

    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = math.sqrt(sum(a * a for a in vec1))
    mag2 = math.sqrt(sum(b * b for b in vec2))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return dot / (mag1 * mag2)


def search_similar_code(code_fact):
    """
    Temporary starter function for RAG retrieval.
    Later this will query a vector database.
    """

    query_text = code_fact.get("snippet") if isinstance(code_fact, dict) else str(code_fact)
    if not query_text:
        query_text = str(code_fact)

    query_embedding = create_embeddings(query_text).get("embedding", [])

    best_match = None
    best_score = -1.0

    for item in INDEX:
        score = cosine_similarity(query_embedding, item.get("embedding", []))
        if score > best_score:
            best_score = score
            best_match = item

    if best_match is None:
        return {
            "query": code_fact,
            "best_match": None
        }

    return {
        "query": code_fact,
        "best_match": {
            "file_path": best_match["file_path"],
            "score": best_score,
            "snippet": best_match["content"][:200]
        }
    }
