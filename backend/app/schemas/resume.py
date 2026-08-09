from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    filename: str
    stored_filename: str
    file_size: int
    content_type: str
    status: str


class ResumePage(BaseModel):
    page_number: int
    text: str


class ResumeExtractionResponse(BaseModel):
    stored_filename: str
    page_count: int
    pages: list[ResumePage]