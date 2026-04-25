from fastapi import APIRouter, HTTPException, Depends

from app.schemas.query import QueryRequest, QueryResponse
from app.services.rag_pipeline import RAGPipeline
from app.api.dependencies import get_current_user

router = APIRouter()


@router.post("/ask", response_model=QueryResponse)
async def ask_question(
    request: QueryRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        user_email = current_user["email"]

        rag_pipeline = RAGPipeline()

        result = rag_pipeline.ask(
            question=request.question,
            top_k=request.top_k,
            source=request.source,
            history=[msg.dict() for msg in request.history],
            user_email=user_email
        )

        return QueryResponse(
            question=request.question,
            rewritten_question=result["rewritten_question"],
            answer=result["answer"],
            cited_answer=result["cited_answer"],
            sources=result["sources"],
            retrieved_chunks=result["retrieved_chunks"],
            message="Answer generated successfully from current user workspace"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")