"""Safe in-memory extraction for text-based PDF and DOCX resumes."""
from io import BytesIO
from pathlib import PurePath

from pypdf import PdfReader
from docx import Document

MAX_FILE_BYTES = 5 * 1024 * 1024


class ResumeParseError(ValueError):
    """Raised when an uploaded resume cannot be safely parsed."""


def extract_resume_text(file_bytes: bytes, filename: str) -> str:
    if not isinstance(file_bytes, bytes) or not file_bytes:
        raise ResumeParseError("The uploaded file is empty or invalid.")
    if len(file_bytes) > MAX_FILE_BYTES:
        raise ResumeParseError("File exceeds the 5 MB upload limit.")
    extension = PurePath(filename or "").suffix.lower()
    try:
        if extension == ".pdf":
            if not file_bytes.startswith(b"%PDF"):
                raise ResumeParseError("The file extension says PDF, but the content is not a valid PDF.")
            reader = PdfReader(BytesIO(file_bytes), strict=True)
            if reader.is_encrypted:
                raise ResumeParseError("Password-protected PDFs are not supported.")
            pages = []
            for page in reader.pages:
                pages.append(page.extract_text() or "")
            return "\n".join(pages)
        if extension == ".docx":
            if not file_bytes.startswith(b"PK"):
                raise ResumeParseError("The file extension says DOCX, but the content is not a valid DOCX file.")
            doc = Document(BytesIO(file_bytes))
            parts = [p.text for p in doc.paragraphs if p.text]
            for table in doc.tables:
                for row in table.rows:
                    parts.append(" | ".join(cell.text for cell in row.cells))
            return "\n".join(parts)
        raise ResumeParseError("Unsupported file type. Upload a PDF or DOCX resume.")
    except ResumeParseError:
        raise
    except Exception as exc:
        raise ResumeParseError("Could not read this resume. Check that the file is valid and not corrupted.") from exc
