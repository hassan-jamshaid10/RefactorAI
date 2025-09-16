from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class IndexRequest(BaseModel):
    repo_url: str

class IndexResponse(BaseModel):
    status: str
    chunks_indexed: int
    repo: str

class ChatRequest(BaseModel):
    query: str
    model: Optional[str] = "phi3"  # default to phi3

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
