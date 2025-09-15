from app import embeddings, vectorstore

def retrieve(query: str, k: int = 5):
    query_emb = embeddings.embed_chunks([{"content": query}])[0]
    return vectorstore.search(query_emb, k)
