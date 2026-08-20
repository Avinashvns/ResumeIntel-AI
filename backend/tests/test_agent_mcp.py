import pytest

from app.agent.graph import (
    build_resume_agent,
)


DOCUMENT_ID = (
    "2be45ab799dc4d879e7ca430c9650b28"
)


@pytest.mark.anyio
async def test_agent_retrieves_context_through_mcp() -> None:

    agent = build_resume_agent()

    result = await agent.ainvoke(
        {
            "document_id": DOCUMENT_ID,
            "query": (
                "Does the candidate have "
                "experience with ML?"
            ),
            "retrieved_context": "",
            "answer": "",
            "sources": [],
            "messages": [],
        },
        config={
            "configurable": {
                "thread_id": "agent-mcp-test",
            }
        },
    )

    assert result["document_id"] == DOCUMENT_ID

    assert result["query"] == (
        "Does the candidate have "
        "experience with ML?"
    )

    assert result["retrieved_context"]

    assert isinstance(
        result["retrieved_context"],
        str,
    )

    assert result["answer"]

    assert isinstance(
        result["answer"],
        str,
    )

    assert result["sources"]

    print("\nMCP Agent Context:")
    print(result["retrieved_context"])

    print("\nAgent Answer:")
    print(result["answer"])


@pytest.mark.anyio
async def test_agent_rejects_empty_query() -> None:

    agent = build_resume_agent()

    with pytest.raises(
        ValueError,
        match=r"Query cannot be empty\.",
    ):
        await agent.ainvoke(
            {
                "document_id": DOCUMENT_ID,
                "query": "",
                "retrieved_context": "",
                "answer": "",
                "sources": [],
                "messages": [],
            },
            config={
                "configurable": {
                    "thread_id": (
                        "agent-mcp-empty-query-test"
                    ),
                }
            },
        )