from app.agent.graph import (
    build_resume_agent,
)


DOCUMENT_ID = (
    "2be45ab799dc4d879e7ca430c9650b28"
)


def test_resume_agent_graph() -> None:

    agent = build_resume_agent()

    result = agent.invoke(
        {
            "document_id": DOCUMENT_ID,
            "query": (
                "Does the candidate have "
                "experience with RAG?"
            ),
            "retrieved_context": "",
            "answer": "",
        }
    )

    assert result["document_id"] == DOCUMENT_ID

    assert (
        result["query"]
        == "Does the candidate have "
        "experience with RAG?"
    )

    assert "retrieved_context" in result
    assert "answer" in result



def test_resume_agent_rejects_empty_query() -> None:

    agent = build_resume_agent()

    try:
        agent.invoke(
            {
                "document_id": DOCUMENT_ID,
                "query": "",
                "retrieved_context": "",
                "answer": "",
            }
        )
    except ValueError as exc:
        assert str(exc) == "Query cannot be empty."
    else:
        raise AssertionError(
            "Expected ValueError for empty query."
        )