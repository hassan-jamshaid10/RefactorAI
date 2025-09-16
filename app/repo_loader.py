import os
import subprocess
from huggingface_hub import snapshot_download

def download_repo(repo_url: str, repo_dir="./repos") -> str:
    os.makedirs(repo_dir, exist_ok=True)

    if "github.com" in repo_url or "gitlab" in repo_url or "bitbucket" in repo_url:
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        local_path = os.path.join(repo_dir, repo_name)

        if not os.path.exists(local_path):
            subprocess.run(["git", "clone", repo_url, local_path], check=True)
        else:
            subprocess.run(["git", "-C", local_path, "pull"], check=True)

    elif "huggingface.co" in repo_url:
        repo_name = repo_url.split("/")[-1]
        local_path = os.path.join(repo_dir, repo_name)

        if not os.path.exists(local_path):
            snapshot_download(repo_url, local_dir=local_path)
    else:
        raise ValueError("Unsupported repo URL")

    return local_path

def load_and_chunk(path: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith((".py", ".md", ".txt", ".json", ".js", ".ts",".jsx", ".java", ".cpp")):
                full_path = os.path.join(root, f)
                try:
                    with open(full_path, "r", encoding="utf-8") as file:
                        text = file.read()
                        for i in range(0, len(text), chunk_size - overlap):
                            chunks.append({"file": full_path, "content": text[i:i+chunk_size]})
                except Exception:
                    pass
    return chunks
