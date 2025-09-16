import numpy as np
from app import vectorstore
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, top_k=5):
    data = vectorstore.get()
    if not data["chunks"]:
        return []
    query_vec = embedder.encode([query])[0]
    scores = np.dot(data["embeddings"], query_vec) / (
        np.linalg.norm(data["embeddings"], axis=1) * np.linalg.norm(query_vec)
    )
    top_idx = np.argsort(scores)[-top_k:][::-1]
    return [data["chunks"][i] for i in top_idx]
