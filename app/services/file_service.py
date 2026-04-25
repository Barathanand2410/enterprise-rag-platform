import os
from fastapi import UploadFile
from app.core.config import settings


class FileService:
    ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]

    @staticmethod
    def validate_file_type(filename: str):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in FileService.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {ext}. Allowed: {FileService.ALLOWED_EXTENSIONS}"
            )

    @staticmethod
    async def save_upload_file(file: UploadFile) -> str:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        return file_path.replace("\\", "/")