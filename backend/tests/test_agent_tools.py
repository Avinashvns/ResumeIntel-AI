from app.agent.tools import search_resume


DOCUMENT_ID = (
    "2be45ab799dc4d879e7ca430c9650b28"
)


def test_search_resume_tool() -> None:

    result = search_resume.invoke(
        {
            "document_id": DOCUMENT_ID,
            "query": (
                "Does the candidate have "
                "experience with ML?"
            ),
            "k": 4,
        }
    )

    assert result
    assert isinstance(result, str)
    assert "Source" in result


def test_search_resume_tool_rejects_empty_query() -> None:

    try:
        search_resume.invoke(
            {
                "document_id": DOCUMENT_ID,
                "query": "",
                "k": 4,
            }
        )
    except ValueError as exc:
        assert str(exc) == "query cannot be empty."
    else:
        raise AssertionError(
            "Expected ValueError for empty query."
        )


def test_search_resume_tool_schema() -> None:

    assert search_resume.name == "search_resume"

    assert search_resume.description

    schema = search_resume.args_schema

    assert "document_id" in schema.model_fields
    assert "query" in schema.model_fields
    assert "k" in schema.model_fields