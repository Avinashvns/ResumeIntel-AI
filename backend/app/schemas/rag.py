from pydantic import BaseModel, Field


class RAGRetrievalRequest(BaseModel):
    query: str = Field(
        min_length=1,
        description="Question to search against the resume.",
    )

    k: int = Field(
        default=4,
        ge=1,
        le=10,
        description="Number of relevant chunks to retrieve.",
    )


class RAGRetrievedDocument(BaseModel):
    chunk_id: str
    text: str
    metadata: dict


class RAGRetrievalResponse(BaseModel):
    document_id: str
    query: str
    result_count: int
    results: list[RAGRetrievedDocument]


class RAGAnswerRequest(BaseModel):
    query: str = Field(
        min_length=1,
        description="Question to ask about the resume.",
    )

    k: int = Field(
        default=4,
        ge=1,
        le=10,
        description="Number of resume chunks used as context.",
    )


class RAGSource(BaseModel):
    chunk_id: str
    page_number: int | str
    text: str


class RAGAnswerResponse(BaseModel):
    document_id: str
    query: str
    answer: str
    sources: list[RAGSource]
