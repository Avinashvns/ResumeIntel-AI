from app.agent.graph import (
    build_resume_agent,
)

DOCUMENT_ID = "2be45ab799dc4d879e7ca430c9650b28"


def test_resume_analysis_agent() -> None:
    agent = build_resume_agent()

    result = agent.invoke(
        {
            "document_id": DOCUMENT_ID,
            "query": ("Does the candidate have experience with ML?"),
            "retrieved_context": "",
            "answer": "",
            "sources": [],
            "messages": [],
        },
        config={
            "configurable": {
                "thread_id": "resume-agent-test",
            }
        },
    )

    assert result["document_id"] == DOCUMENT_ID

    assert result["query"] == ("Does the candidate have experience with ML?")

    assert result["retrieved_context"]

    assert result["answer"]

    assert isinstance(
        result["answer"],
        str,
    )

    assert result["sources"]

    print("\nAgent Answer:")
    print(result["answer"])

    print("\nAgent Sources:")

    for source in result["sources"]:
        print(f"Page {source['page_number']} | {source['chunk_id']}")


def test_resume_analysis_agent_rejects_empty_query() -> None:
    agent = build_resume_agent()

    try:
        agent.invoke(
            {
                "document_id": DOCUMENT_ID,
                "query": "",
                "retrieved_context": "",
                "answer": "",
                "sources": [],
            }
        )
    except ValueError as exc:
        assert str(exc) == "Query cannot be empty."
    else:
        raise AssertionError("Expected ValueError for empty query.")
