from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    texts = [c["content"] for c in chunks]
    return model.encode(texts, convert_to_numpy=True).tolist()
