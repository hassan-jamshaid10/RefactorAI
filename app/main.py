from fastapi import FastAPI
from app import repo_loader, embeddings, vectorstore, retriever, rag
from app.models import ChatRequest, ChatResponse, IndexRequest, IndexResponse

app = FastAPI(
    title="Local RAG Chatbot (Phi-3 + Ollama)",
    description="Offline RAG chatbot using Phi-3 (via Ollama) and HuggingFace embeddings",
    version="1.0.0"
)

@app.post("/index_repo", response_model=IndexResponse, summary="Index a GitHub/HF repo")
async def index_repo(request: IndexRequest):
    local_path = repo_loader.download_repo(request.repo_url)
    chunks = repo_loader.load_and_chunk(local_path)
    embeddings_list = embeddings.embed_chunks(chunks)
    vectorstore.store(chunks, embeddings_list)
    return {"status": "indexed", "chunks_indexed": len(chunks), "repo": request.repo_url}

@app.post("/chat", response_model=ChatResponse, summary="Chat with your codebase")
async def chat(request: ChatRequest):
    retrieved_chunks = retriever.retrieve(request.query)
    answer, sources = rag.generate_answer(request.query, retrieved_chunks, request.model or "phi3")
    formatted_sources = [
        {"file": c["file"], "snippet": c["content"][:120]} for c in retrieved_chunks
    ]
    return ChatResponse(answer=answer, sources=formatted_sources)
