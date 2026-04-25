from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ChatMessage(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3
    source: Optional[str] = None
    history: List[ChatMessage] = []


class QueryResponse(BaseModel):
    question: str
    rewritten_question: str
    answer: str
    cited_answer: str
    sources: List[Dict[str, Any]]
    retrieved_chunks: List[str]
    message: str