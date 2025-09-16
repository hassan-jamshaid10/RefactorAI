import numpy as np

store_data = {"chunks": [], "embeddings": []}

def store(chunks, embeddings):
    if len(embeddings) == 0:
        raise ValueError("No embeddings generated")
    store_data["chunks"] = chunks
    store_data["embeddings"] = embeddings

def get():
    return store_data
