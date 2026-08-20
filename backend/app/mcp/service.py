from app.mcp.client import call_mcp_tool


async def search_resume_via_mcp(
    document_id: str,
    query: str,
    k: int = 4,
) -> str:
    """
    Search a resume through the ResumeIntel
    MCP server.
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

    result = await call_mcp_tool(
        tool_name="search_resume",
        arguments={
            "document_id": document_id,
            "query": query,
            "k": k,
        },
    )

    if result.is_error:
        error_text = "\n".join(
            content.text
            for content in result.content
            if hasattr(content, "text")
        )

        raise RuntimeError(
            f"MCP search_resume tool failed: "
            f"{error_text}"
        )

    if not result.content:
        return ""

    text_parts: list[str] = []

    for content in result.content:
        if hasattr(content, "text"):
            text_parts.append(
                content.text
            )

    return "\n\n".join(text_parts)