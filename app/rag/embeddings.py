from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(text):
    embedding = _model.encode(text).tolist()
    return {
        "text": text,
        "embedding": embedding
    }