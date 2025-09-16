import requests

def generate_answer(query, retrieved_chunks, model="phi3"):
    context = "\n".join([c["content"] for c in retrieved_chunks])
    prompt = f"Query: {query}\nContext:\n{context}"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        answer = response.json().get("response", "").strip()
    except Exception as e:
        answer = f"Error running model: {e}"

    return answer, retrieved_chunks
