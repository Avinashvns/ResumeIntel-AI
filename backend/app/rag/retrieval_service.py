from langchain_core.documents import Document

from app.retrieval.retriever import (
    retrieve_resume_documents,
)


def retrieve_resume_context(
    document_id: str,
    query: str,
    k: int = 4,
) -> list[Document]:
    """
    Retrieve relevant resume documents
    for a user query.
    """

    if not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    if k < 1:
        raise ValueError(
            "k must be greater than 0."
        )

    return retrieve_resume_documents(
        document_id=document_id,
        query=query,
        k=k,
    )