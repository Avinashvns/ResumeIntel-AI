from langchain_core.documents import Document


def format_documents_as_context(
    documents: list[Document],
) -> str:
    """
    Convert retrieved LangChain Documents
    into a formatted context string.
    """

    if not documents:
        return ""

    context_parts: list[str] = []

    for index, document in enumerate(
        documents,
        start=1,
    ):
        metadata = document.metadata

        page_number = metadata.get(
            "page_number",
            "unknown",
        )

        chunk_id = metadata.get(
            "chunk_id",
            f"chunk-{index}",
        )

        context_parts.append(
            (
                f"[Source {index}]\n"
                f"Chunk ID: {chunk_id}\n"
                f"Page: {page_number}\n"
                f"Content:\n"
                f"{document.page_content}"
            )
        )

    return "\n\n".join(context_parts)