import uuid
from typing import List, Optional

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import settings
from app.services.embedding_service import EmbeddingService


class VectorStoreService:
    def __init__(self):
        self.embedding_model = EmbeddingService().get_model()

        self.vector_store = Chroma(
            collection_name=settings.VECTOR_COLLECTION_NAME,
            embedding_function=self.embedding_model,
            persist_directory=settings.VECTOR_DB_DIR
        )

    def add_chunks(self, chunks: List[str], source_name: str, user_email: str) -> int:
        ids = []
        texts = []
        metadatas = []

        for idx, chunk in enumerate(chunks):
            ids.append(str(uuid.uuid4()))
            texts.append(chunk)
            metadatas.append({
                "source": source_name,
                "chunk_index": idx,
                "user_email": user_email
            })

        self.vector_store.add_texts(
            texts=texts,
            metadatas=metadatas,
            ids=ids
        )

        return len(texts)

    def search(
        self,
        query: str,
        top_k: int = 3,
        source: Optional[str] = None,
        user_email: Optional[str] = None
    ) -> List[Document]:

        filter_query = {}

        if user_email:
            filter_query["user_email"] = user_email

        if source:
            filter_query["source"] = source

        if filter_query:
            results = self.vector_store.similarity_search(
                query=query,
                k=top_k,
                filter=filter_query
            )
        else:
            results = self.vector_store.similarity_search(
                query=query,
                k=top_k
            )

        return results

    def delete_by_source(self, source_name: str, user_email: str) -> int:
        results = self.vector_store.get(
            where={
                "$and": [
                    {"source": source_name},
                    {"user_email": user_email}
                ]
            }
        )

        ids = results.get("ids", [])

        if ids:
            self.vector_store.delete(ids=ids)

        return len(ids)

    def count_documents(self, user_email: str) -> int:
        results = self.vector_store.get(
            where={"user_email": user_email}
        )

        ids = results.get("ids", [])
        return len(ids)

    def list_sources(self, user_email: str):
        results = self.vector_store.get(
            where={"user_email": user_email}
        )

        metadatas = results.get("metadatas", [])
        source_map = {}

        for metadata in metadatas:
            source_name = metadata.get("source", "unknown")
            source_map[source_name] = source_map.get(source_name, 0) + 1

        return [
            {"source": source, "chunk_count": count}
            for source, count in source_map.items()
        ]