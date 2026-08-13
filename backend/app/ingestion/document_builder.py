from langchain_core.documents import Document


def build_resume_document(
    text: str,
    document_id: str,
    filename: str,
    page_number: int,
    chunk_id: str,
    section: str | None = None,
) -> Document:
    """
    Create a LangChain Document for a resume chunk.
    """

    metadata = {
        "document_id": document_id,
        "filename": filename,
        "source": filename,
        "page_number": page_number,
        "chunk_id": chunk_id,
    }

    if section:
        metadata["section"] = section

    return Document(
        page_content=text,
        metadata=metadata,
    )