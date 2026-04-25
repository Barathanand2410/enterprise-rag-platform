from fastapi import APIRouter, HTTPException, Query, Depends

from app.schemas.admin import (
    ListDocumentsResponse,
    DeleteDocumentResponse,
    StatsResponse,
    IndexedDocument
)
from app.services.vector_store import VectorStoreService
from app.api.dependencies import get_current_user

router = APIRouter()


@router.get("/documents", response_model=ListDocumentsResponse)
async def list_documents(
    current_user: dict = Depends(get_current_user)
):
    try:
        user_email = current_user["email"]

        vector_store = VectorStoreService()
        documents = vector_store.list_sources(user_email=user_email)
        total_chunks = vector_store.count_documents(user_email=user_email)

        return ListDocumentsResponse(
            total_documents=len(documents),
            total_chunks=total_chunks,
            documents=[IndexedDocument(**doc) for doc in documents],
            message="Indexed documents retrieved successfully for current user"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.delete("/documents", response_model=DeleteDocumentResponse)
async def delete_document(
    source: str = Query(..., description="Source file name to delete"),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_email = current_user["email"]

        vector_store = VectorStoreService()
        deleted_count = vector_store.delete_by_source(
            source_name=source,
            user_email=user_email
        )

        return DeleteDocumentResponse(
            source=source,
            deleted_chunks=deleted_count,
            message="Document deleted successfully from current user workspace"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/stats", response_model=StatsResponse)
async def get_stats(
    current_user: dict = Depends(get_current_user)
):
    try:
        user_email = current_user["email"]

        vector_store = VectorStoreService()
        total_chunks = vector_store.count_documents(user_email=user_email)

        return StatsResponse(
            total_chunks=total_chunks,
            message="Current user vector database stats retrieved successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")