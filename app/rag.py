# import google.generativeai as genai
# import os


# genai.configure(api_key="AIzaSyCf2MWy2IJ8wY2Qs-__xQnMxmZFFNJAKSk")

# def generate_answer(query, retrieved_chunks):
#     context_text = "\n\n".join(
#         [f"[{c['file']}]\n{c['content']}" for c in retrieved_chunks]
#     )
#     prompt = f"""
#     You are a code assistant. Answer the user query based ONLY on the provided context.
#     Always cite sources with [file].
    
#     Query: {query}
#     Context:
#     {context_text}
#     """
#     resp = genai.generate_content(
#         model="gemini-1.5-pro",
#         contents=prompt
#     )
#     return resp.text, [{"file": c["file"]} for c in retrieved_chunks]
import requests

# Direct API key (⚠️ replace with your key)
GEMINI_API_KEY = "AIzaSyC_qDtrQeBtbTM1vtY0UK-_FjHcdna94hY"
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def generate_answer(query, retrieved_chunks):
    context_text = "\n\n".join(
        [f"[{c['file']}]\n{c['content']}" for c in retrieved_chunks]
    )

    prompt = f"""
    You are a code assistant. Answer the user query based ONLY on the provided context.
    Always cite sources in the format [file].

    Query: {query}

    Context:
    {context_text}
    """

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(GEMINI_ENDPOINT, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.text}", []

    data = response.json()

    # Extract answer safely
    try:
        answer_text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        answer_text = "No valid response from Gemini."

    sources = [{"file": c["file"]} for c in retrieved_chunks]
    return answer_text, sources
