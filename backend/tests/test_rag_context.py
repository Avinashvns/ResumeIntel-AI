from langchain_core.documents import Document

from app.rag.context import (
    format_documents_as_context,
)


def test_format_documents_as_context() -> None:

    documents = [
        Document(
            page_content=(
                "Built a RAG application."
            ),
            metadata={
                "chunk_id": "page-2-chunk-1",
                "page_number": 2,
            },
        ),
        Document(
            page_content=(
                "Used LangChain and FAISS."
            ),
            metadata={
                "chunk_id": "page-3-chunk-1",
                "page_number": 3,
            },
        ),
    ]

    context = format_documents_as_context(
        documents
    )

    assert "page-2-chunk-1" in context
    assert "page-3-chunk-1" in context
    assert "Built a RAG application." in context
    assert "Used LangChain and FAISS." in context