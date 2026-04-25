from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing in .env")

        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )

    def get_model(self):
        return self.embedding_model

    def embed_chunks(self, chunks: list[str]):
        return self.embedding_model.embed_documents(chunks)

    def embed_query(self, query: str):
        return self.embedding_model.embed_query(query)