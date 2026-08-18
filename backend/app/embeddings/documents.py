from langchain_core.documents import Document

from app.embeddings.model import generate_embeddings


def embed_documents(
    documents: list[Document],
) -> list[list[float]]:
    """
    Generate embeddings for LangChain Documents.
    """

    if not documents:
        return []

    texts = [
        document.page_content
        for document in documents
    ]

    return generate_embeddings(texts)