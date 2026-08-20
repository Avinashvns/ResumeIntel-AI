from pydantic import BaseModel, Field


class AgentAskRequest(BaseModel):
    query: str = Field(
        min_length=1,
        description="Question to ask about the resume.",
    )

    thread_id: str = Field(
        min_length=1,
        description="Conversation thread identifier.",
    )


class AgentSource(BaseModel):
    chunk_id: str
    page_number: int | str
    text: str


class AgentAskResponse(BaseModel):
    document_id: str
    query: str
    answer: str
    sources: list[AgentSource]
    thread_id: str