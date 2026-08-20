import asyncio

from langchain_core.tools import tool

from app.mcp.service import (
    search_resume_via_mcp,
)


@tool
def search_resume(
    document_id: str,
    query: str,
    k: int = 4,
) -> str:
    """
    Search an uploaded resume through the
    ResumeIntel MCP server.

    Use this tool whenever resume evidence
    is needed.
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

    return asyncio.run(
        search_resume_via_mcp(
            document_id=document_id,
            query=query,
            k=k,
        )
    )