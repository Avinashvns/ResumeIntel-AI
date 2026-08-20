from langchain_core.messages import (
    HumanMessage,
)

from app.agent.graph import (
    build_resume_agent,
)


DOCUMENT_ID = (
    "2be45ab799dc4d879e7ca430c9650b28"
)


def test_agent_memory() -> None:

    agent = build_resume_agent()

    config = {
        "configurable": {
            "thread_id": "resume-memory-test",
        }
    }

    first_result = agent.invoke(
        {
            "document_id": DOCUMENT_ID,
            "query": (
                "Does the candidate have "
                "experience with RAG?"
            ),
            "retrieved_context": "",
            "answer": "",
            "sources": [],
            "messages": [
                HumanMessage(
                    content=(
                        "Does the candidate have "
                        "experience with RAG?"
                    )
                )
            ],
        },
        config=config,
    )

    assert first_result["answer"]

    second_result = agent.invoke(
        {
            "document_id": DOCUMENT_ID,
            "query": (
                "Which technologies were used "
                "for that?"
            ),
            "retrieved_context": "",
            "answer": "",
            "sources": [],
            "messages": [
                HumanMessage(
                    content=(
                        "Which technologies were used "
                        "for that?"
                    )
                )
            ],
        },
        config=config,
    )

    assert second_result["answer"]

    assert len(
        second_result["messages"]
    ) >= 2