"""
Tests for VIDYA pdf_reader module.
Run with: pytest tests/test_pdf_reader.py
"""

import io
import pytest

# Make modules importable from the parent directory
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.pdf_reader import extract_text, page_count, PDFExtractionError


def _make_minimal_pdf() -> bytes:
    """Create a minimal valid text-based PDF in memory without external libraries."""
    try:
        from pypdf import PdfWriter
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        buf = io.BytesIO()
        writer.write(buf)
        return buf.getvalue()
    except ImportError:
        pytest.skip("pypdf not installed")


def test_extract_text_invalid_bytes_raises():
    with pytest.raises(PDFExtractionError):
        extract_text(b"not a pdf at all")


def test_page_count_invalid_returns_zero():
    assert page_count(b"garbage") == 0


def test_page_count_valid_pdf():
    pdf_bytes = _make_minimal_pdf()
    assert page_count(pdf_bytes) >= 1


def test_extract_text_empty_pdf_raises():
    """A blank page PDF has no extractable text."""
    pdf_bytes = _make_minimal_pdf()
    with pytest.raises(PDFExtractionError, match="No readable text"):
        extract_text(pdf_bytes)
