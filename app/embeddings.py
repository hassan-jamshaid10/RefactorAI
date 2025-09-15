import requests

# Direct API key (⚠️ replace with your key)
GEMINI_API_KEY = "AIzaSyC_qDtrQeBtbTM1vtY0UK-_FjHcdna94hY"
EMBEDDING_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent"

def embed_chunks(chunks):
    embeddings = []
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    for chunk in chunks:
        payload = {
            "model": "models/embedding-001",
            "content": {"parts": [{"text": chunk["content"]}]}
        }
        response = requests.post(EMBEDDING_ENDPOINT, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Embedding failed: {response.text}")

        data = response.json()
        vector = data["embedding"]["value"]
        chunk["embedding"] = vector
        embeddings.append(vector)

    return embeddings
