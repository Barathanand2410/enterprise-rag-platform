from pydantic import BaseModel
from typing import List


class UploadResponse(BaseModel):
    filename: str
    file_path: str
    extracted_characters: int
    total_chunks: int
    chunks_indexed: int
    preview: str
    sample_chunks: List[str]
    message: str