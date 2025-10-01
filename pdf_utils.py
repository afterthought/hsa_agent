"""
PDF Utilities for Healthcare Bill Processing

Provides functions to scan for PDFs and extract text content.
"""

import os
from pathlib import Path
from typing import List
import pdfplumber
import PyPDF2


def scan_for_pdfs(directory: str, recursive: bool = True) -> List[str]:
    """
    Scan a directory for PDF files.

    Args:
        directory: Path to the directory to scan
        recursive: Whether to scan subdirectories recursively

    Returns:
        List of paths to PDF files found
    """
    pdf_files = []
    directory_path = Path(directory).expanduser().resolve()

    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")

    if not directory_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")

    if recursive:
        # Recursively find all PDF files
        for pdf_file in directory_path.rglob("*.pdf"):
            pdf_files.append(str(pdf_file))
    else:
        # Only scan the immediate directory
        for pdf_file in directory_path.glob("*.pdf"):
            pdf_files.append(str(pdf_file))

    # Sort for consistent ordering
    pdf_files.sort()

    return pdf_files


def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.

    Uses pdfplumber as the primary method, with PyPDF2 as a fallback.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text content

    Raises:
        ValueError: If the file doesn't exist or is not a PDF
        Exception: If text extraction fails
    """
    pdf_path = Path(pdf_path).expanduser().resolve()

    if not pdf_path.exists():
        raise ValueError(f"File does not exist: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"File is not a PDF: {pdf_path}")

    text = ""

    # Try pdfplumber first (better for complex layouts)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num} ---\n"
                    text += page_text
                    text += "\n"
    except Exception as e:
        # Fallback to PyPDF2
        try:
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num} ---\n"
                        text += page_text
                        text += "\n"
        except Exception as fallback_error:
            raise Exception(
                f"Failed to extract text using both methods. "
                f"pdfplumber error: {str(e)}, "
                f"PyPDF2 error: {str(fallback_error)}"
            )

    if not text.strip():
        raise Exception("No text could be extracted from the PDF. The PDF might be image-based or encrypted.")

    return text.strip()


def extract_pdf_metadata(pdf_path: str) -> dict:
    """
    Extract metadata from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Dictionary containing PDF metadata
    """
    pdf_path = Path(pdf_path).expanduser().resolve()

    if not pdf_path.exists():
        raise ValueError(f"File does not exist: {pdf_path}")

    metadata = {
        "file_path": str(pdf_path),
        "file_name": pdf_path.name,
        "file_size_bytes": pdf_path.stat().st_size,
    }

    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            metadata["num_pages"] = len(reader.pages)

            if reader.metadata:
                metadata["title"] = reader.metadata.get("/Title", "")
                metadata["author"] = reader.metadata.get("/Author", "")
                metadata["subject"] = reader.metadata.get("/Subject", "")
                metadata["creator"] = reader.metadata.get("/Creator", "")
                metadata["producer"] = reader.metadata.get("/Producer", "")
                metadata["creation_date"] = reader.metadata.get("/CreationDate", "")

    except Exception as e:
        metadata["error"] = f"Failed to extract metadata: {str(e)}"

    return metadata
