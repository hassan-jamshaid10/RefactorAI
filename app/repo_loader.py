import os

def load_and_chunk(repo_path: str, chunk_size: int = 300, overlap: int = 50):
    chunks = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".java", ".md")):
                with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                    # Simple token-based chunking
                    tokens = text.split()
                    for i in range(0, len(tokens), chunk_size - overlap):
                        chunk_text = " ".join(tokens[i:i + chunk_size])
                        chunks.append({
                            "file": os.path.join(root, file),
                            "content": chunk_text
                        })
    return chunks
