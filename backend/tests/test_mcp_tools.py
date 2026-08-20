from app.mcp.server import (
    mcp,
    search_resume,
)


DOCUMENT_ID = (
    "2be45ab799dc4d879e7ca430c9650b28"
)


def test_mcp_server_has_search_resume_tool() -> None:
    assert mcp is not None

    assert search_resume is not None


def test_mcp_search_resume_tool() -> None:

    result = search_resume(
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

    print("\nMCP Search Result:")
    print(result)



def test_mcp_search_resume_rejects_empty_query() -> None:

    try:
        search_resume(
            document_id=DOCUMENT_ID,
            query="",
            k=4,
        )
    except ValueError as exc:
        assert str(exc) == "query cannot be empty."
    else:
        raise AssertionError(
            "Expected ValueError for empty query."
        )