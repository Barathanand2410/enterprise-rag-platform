from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.schemas.ingest import UploadResponse
from app.services.file_service import FileService
from app.services.document_loader import DocumentLoaderService
from app.services.text_splitter import TextSplitterService
from app.services.vector_store import VectorStoreService
from app.api.dependencies import get_current_user

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_email = current_user["email"]

        FileService.validate_file_type(file.filename)
        saved_path = await FileService.save_upload_file(file)

        extracted_text = DocumentLoaderService.load_text(saved_path)

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text could not be extracted from the uploaded document."
            )

        chunks = TextSplitterService.split_text(extracted_text)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No chunks were created from the extracted document text."
            )

        vector_store = VectorStoreService()

        vector_store.delete_by_source(
            source_name=file.filename,
            user_email=user_email
        )

        chunks_indexed = vector_store.add_chunks(
            chunks=chunks,
            source_name=file.filename,
            user_email=user_email
        )

        return UploadResponse(
            filename=file.filename,
            file_path=saved_path.replace("\\", "/"),
            extracted_characters=len(extracted_text),
            total_chunks=len(chunks),
            chunks_indexed=chunks_indexed,
            preview=extracted_text[:500],
            sample_chunks=chunks[:3],
            message="File uploaded, re-indexed safely, and stored in user workspace successfully"
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")