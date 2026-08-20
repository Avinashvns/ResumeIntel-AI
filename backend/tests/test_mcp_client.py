import pytest

from app.mcp.service import (
    search_resume_via_mcp,
)


DOCUMENT_ID = (
    "2be45ab799dc4d879e7ca430c9650b28"
)


@pytest.mark.anyio
async def test_search_resume_via_mcp() -> None:

    result = await search_resume_via_mcp(
        document_id=DOCUMENT_ID,
        query=(
            "Does the candidate have "
            "experience with ML?"
        ),
        k=4,
    )

    assert result

    assert isinstance(
        result,
        str,
    )

    assert "Source" in result

    print("\nMCP Client Result:")
    print(result)


@pytest.mark.anyio
async def test_search_resume_via_mcp_rejects_empty_query() -> None:

    with pytest.raises(
        ValueError,
        match="query cannot be empty.",
    ):
        await search_resume_via_mcp(
            document_id=DOCUMENT_ID,
            query="",
            k=4,
        )