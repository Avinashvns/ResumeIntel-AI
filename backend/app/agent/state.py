from typing import TypedDict


class ResumeAgentState(TypedDict):
    document_id: str
    query: str
    retrieved_context: str
    answer: str
    sources: list[dict]