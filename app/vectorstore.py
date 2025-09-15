import faiss
import numpy as np

index = None
chunk_store = []

def store(chunks, embeddings):
    global index, chunk_store
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    vectors = np.array(embeddings).astype("float32")
    index.add(vectors)
    chunk_store = chunks

def search(query_embedding, k=5):
    global index, chunk_store
    query_vec = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(query_vec, k)
    return [chunk_store[i] for i in indices[0]]
