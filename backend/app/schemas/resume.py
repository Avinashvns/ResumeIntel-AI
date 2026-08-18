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


class ResumeDocument(BaseModel):
    chunk_id: str
    text: str
    metadata: dict


class ResumeDocumentResponse(BaseModel):
    stored_filename: str
    document_count: int
    documents: list[ResumeDocument]

class ResumeIndexResponse(BaseModel):
    stored_filename: str
    document_id: str
    document_count: int
    index_path: str
    status: str


class ResumeRetrievalResult(BaseModel):
    chunk_id: str
    text: str
    metadata: dict


class ResumeRetrievalResponse(BaseModel):
    document_id: str
    query: str
    result_count: int
    results: list[ResumeRetrievalResult]