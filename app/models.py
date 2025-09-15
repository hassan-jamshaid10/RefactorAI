from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ChatRequest(BaseModel):
    query: str = Field(..., example="Explain how authentication works in the repo")
    persona: str = Field(
        default="senior_engineer",
        example="mentor",
        description="Choose chatbot persona: senior_engineer, mentor, reviewer"
    )

class Source(BaseModel):
    file: str = Field(..., example="src/auth/middleware.py")
    snippet: Optional[str] = Field(None, example="def verify_token(token): ...")

class ChatResponse(BaseModel):
    answer: str = Field(..., example="The authentication flow starts with middleware...")
    sources: List[Source] = Field(
        ...,
        description="List of source files/snippets used for this answer"
    )

class IndexResponse(BaseModel):
    status: str = Field(..., example="indexed")
    chunks_indexed: int = Field(..., example=152)
