"""
VIDYA – pdf_reader.py
Extract text from uploaded PDF files using pypdf.
"""

from __future__ import annotations
import io

try:
    from pypdf import PdfReader as _PdfReader
    _PYPDF_AVAILABLE = True
except ImportError:
    _PYPDF_AVAILABLE = False


class PDFExtractionError(Exception):
    """Raised when text extraction fails for any reason."""


def extract_text(file_bytes: bytes) -> str:
    """
    Extract plain text from a PDF supplied as raw bytes.

    Returns the extracted text string (may be empty for scanned PDFs).
    Raises PDFExtractionError with a user-friendly message on failure.
    """
    if not _PYPDF_AVAILABLE:
        raise PDFExtractionError(
            "The pypdf library is not installed. "
            "Run `pip install pypdf` and restart the application."
        )

    try:
        reader = _PdfReader(io.BytesIO(file_bytes))
    except Exception as exc:
        raise PDFExtractionError(f"Could not open PDF file: {exc}") from exc

    if len(reader.pages) == 0:
        raise PDFExtractionError("The PDF contains no pages.")

    parts: list[str] = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        if text.strip():
            parts.append(text)

    if not parts:
        raise PDFExtractionError(
            "No readable text was found in this PDF. "
            "It may be a scanned image-only document. "
            "OCR is not currently supported — please use a text-based PDF."
        )

    return "\n\n".join(parts)


def page_count(file_bytes: bytes) -> int:
    """Return the number of pages in the PDF, or 0 on error."""
    if not _PYPDF_AVAILABLE:
        return 0
    try:
        reader = _PdfReader(io.BytesIO(file_bytes))
        return len(reader.pages)
    except Exception:
        return 0
