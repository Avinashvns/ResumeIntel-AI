from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ingestion.storage import (
    generate_stored_filename,
    get_resume_path,
)
from app.schemas.resume import ResumeUploadResponse


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