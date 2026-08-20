from pathlib import Path

import pymupdf


class PDFExtractionError(Exception):
    """Raised when PDF text extraction fails."""


def extract_pdf_text(file_path: Path) -> list[dict]:
    """
    Extract text from a PDF page by page.

    Returns:
        A list containing page number and extracted text.
    """

    if not file_path.exists():
        raise PDFExtractionError(
            f"PDF file not found: {file_path}"
        )

    try:
        document = pymupdf.open(file_path)

        pages = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

        document.close()

        return pages

    except Exception as exc:
        raise PDFExtractionError(
            "Failed to extract text from PDF."
        ) from exc