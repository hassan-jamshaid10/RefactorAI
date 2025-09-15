from fastapi import FastAPI, UploadFile, Form
from app import repo_loader, embeddings, vectorstore, retriever, rag
from app.models import ChatRequest, ChatResponse, IndexResponse

app = FastAPI(
    title="RAG Chatbot (Gemini-powered)",
    description="Chatbot for exploring code repositories using Retrieval-Augmented Generation (RAG) and Google Gemini API.",
    version="1.1.0",
    contact={
        "name": "Your Team",
        "url": "https://yourcompany.com",
        "email": "dev@yourcompany.com",
    }
)

@app.post(
    "/index_repo",
    response_model=IndexResponse,
    summary="Index a repository",
    description="Ingests a local repo path, chunks the code, generates embeddings with Gemini, and stores them in FAISS."
)
async def index_repo(repo_path: str = Form(..., description="Path to local repository")):
    chunks = repo_loader.load_and_chunk(repo_path)
    embeddings_list = embeddings.embed_chunks(chunks)
    vectorstore.store(chunks, embeddings_list)
    return {"status": "indexed", "chunks_indexed": len(chunks)}

@app.post(
    "/chat",
    response_model=ChatResponse,
    summary="Ask a question about the repo",
    description="Retrieves relevant code chunks using RAG and generates a Gemini-powered response with citations."
)
async def chat(request: ChatRequest):
    retrieved_chunks = retriever.retrieve(request.query)
    answer, sources = rag.generate_answer(request.query, retrieved_chunks)
    # Format sources with snippets for better UX
    formatted_sources = [
        {"file": c["file"], "snippet": c["content"][:120]} for c in retrieved_chunks
    ]
    return ChatResponse(answer=answer, sources=formatted_sources)
