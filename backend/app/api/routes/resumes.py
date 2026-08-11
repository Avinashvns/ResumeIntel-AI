from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ingestion.storage import (
    generate_stored_filename,
    get_resume_path,
)

from app.ingestion.pdf_extractor import (
    PDFExtractionError,
    extract_pdf_text,
)
from app.schemas.resume import (
    CleanedResumePage,
    ResumeExtractionResponse,
    ResumePage,
    ResumeUploadResponse,
    ResumeCleaningResponse,
)

from app.ingestion.text_cleaner import clean_text


router = APIRouter(
    prefix="/api/v1/resumes",
    tags=["Resumes"],
)


MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_CONTENT_TYPE = "application/pdf"


@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
)
async def upload_resume(
    file: UploadFile = File(...),
) -> ResumeUploadResponse:

    if file.content_type != ALLOWED_CONTENT_TYPE:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="File must have a .pdf extension.",
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    file_size = len(content)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Resume file must be smaller than 5 MB.",
        )

    stored_filename = generate_stored_filename(
        file.filename
    )

    file_path = get_resume_path(stored_filename)

    file_path.write_bytes(content)

    return ResumeUploadResponse(
        filename=file.filename,
        stored_filename=stored_filename,
        file_size=file_size,
        content_type=file.content_type,
        status="uploaded",
    )


@router.get(
    "/{stored_filename}/text",
    response_model=ResumeExtractionResponse,
)
def extract_resume_text(
    stored_filename: str,
) -> ResumeExtractionResponse:

    file_path = get_resume_path(stored_filename)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Resume file not found.",
        )

    try:
        pages = extract_pdf_text(file_path)

    except PDFExtractionError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return ResumeExtractionResponse(
        stored_filename=stored_filename,
        page_count=len(pages),
        pages=[
            ResumePage(**page)
            for page in pages
        ],
    )


@router.get(
    "/{stored_filename}/clean",
    response_model=ResumeCleaningResponse,
)
def clean_resume_text(
    stored_filename: str,
) -> ResumeCleaningResponse:

    file_path = get_resume_path(stored_filename)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Resume file not found.",
        )

    try:
        pages = extract_pdf_text(file_path)

    except PDFExtractionError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    cleaned_pages = [
        CleanedResumePage(
            page_number=page["page_number"],
            text=clean_text(page["text"]),
        )
        for page in pages
    ]

    return ResumeCleaningResponse(
        stored_filename=stored_filename,
        page_count=len(cleaned_pages),
        pages=cleaned_pages,
    )