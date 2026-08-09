from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    filename: str
    stored_filename: str
    file_size: int
    content_type: str
    status: str