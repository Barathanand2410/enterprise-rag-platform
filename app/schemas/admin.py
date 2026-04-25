from pydantic import BaseModel
from typing import List


class IndexedDocument(BaseModel):
    source: str
    chunk_count: int


class ListDocumentsResponse(BaseModel):
    total_documents: int
    total_chunks: int
    documents: List[IndexedDocument]
    message: str


class DeleteDocumentResponse(BaseModel):
    source: str
    deleted_chunks: int
    message: str


class StatsResponse(BaseModel):
    total_chunks: int
    message: str