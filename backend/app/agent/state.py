from typing import Annotated, TypedDict

from langchain_core.messages import (
    BaseMessage,
)
from langgraph.graph.message import add_messages


class ResumeAgentState(TypedDict):
    document_id: str
    query: str
    retrieved_context: str
    answer: str
    sources: list[dict]
    messages: Annotated[
        list[BaseMessage],
        add_messages,
    ]
