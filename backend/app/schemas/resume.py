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


class CleanedResumePage(BaseModel):
    page_number: int
    text: str


class ResumeCleaningResponse(BaseModel):
    stored_filename: str
    page_count: int
    pages: list[CleanedResumePage]


class ResumeChunk(BaseModel):
    chunk_id: str
    text: str
    page_number: int


class ResumeChunkingResponse(BaseModel):
    stored_filename: str
    chunk_count: int
    chunks: list[ResumeChunk]