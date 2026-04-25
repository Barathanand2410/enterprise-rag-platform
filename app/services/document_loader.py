from pathlib import Path
from pypdf import PdfReader
from docx import Document


class DocumentLoaderService:
    @staticmethod
    def load_text(file_path: str) -> str:
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return DocumentLoaderService._load_pdf(path)
        elif suffix == ".docx":
            return DocumentLoaderService._load_docx(path)
        elif suffix == ".txt":
            return DocumentLoaderService._load_txt(path)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    @staticmethod
    def _load_pdf(path: Path) -> str:
        reader = PdfReader(str(path))
        texts = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            texts.append(page_text)

        return "\n".join(texts)

    @staticmethod
    def _load_docx(path: Path) -> str:
        doc = Document(str(path))
        return "\n".join([para.text for para in doc.paragraphs])

    @staticmethod
    def _load_txt(path: Path) -> str:
        return path.read_text(encoding="utf-8")