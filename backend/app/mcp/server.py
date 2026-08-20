from mcp.server import MCPServer

from app.retrieval.retriever import (
    retrieve_resume_documents,
)


mcp = MCPServer(
    "ResumeIntel MCP Server"
)


@mcp.tool()
def health_check() -> str:
    """
    Check whether the ResumeIntel MCP server
    is running.
    """

    return "ResumeIntel MCP Server is healthy"


@mcp.tool()
def search_resume(
    document_id: str,
    query: str,
    k: int = 4,
) -> str:
    """
    Search an uploaded resume for information
    relevant to the user's question.

    Returns relevant resume chunks with their
    source metadata.
    """

    if not document_id.strip():
        raise ValueError(
            "document_id cannot be empty."
        )

    if not query.strip():
        raise ValueError(
            "query cannot be empty."
        )

    if k < 1:
        raise ValueError(
            "k must be greater than 0."
        )

    documents = retrieve_resume_documents(
        document_id=document_id,
        query=query,
        k=k,
    )

    if not documents:
        return (
            "No relevant resume information "
            "was found."
        )

    results: list[str] = []

    for index, document in enumerate(
        documents,
        start=1,
    ):
        chunk_id = document.metadata.get(
            "chunk_id",
            f"chunk-{index}",
        )

        page_number = document.metadata.get(
            "page_number",
            "unknown",
        )

        results.append(
            (
                f"[Source {index}]\n"
                f"Chunk ID: {chunk_id}\n"
                f"Page: {page_number}\n"
                f"Content:\n"
                f"{document.page_content}"
            )
        )

    return "\n\n".join(results)


if __name__ == "__main__":
    mcp.run()