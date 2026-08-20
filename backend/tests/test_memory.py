from langchain_core.messages import (
    HumanMessage,
)

from app.agent.memory import (
    get_recent_messages,
)


def test_get_recent_messages() -> None:

    messages = [
        HumanMessage(content="Question 1"),
        HumanMessage(content="Question 2"),
        HumanMessage(content="Question 3"),
    ]

    result = get_recent_messages(
        messages,
        limit=2,
    )

    assert len(result) == 2

    assert result[0].content == "Question 2"
    assert result[1].content == "Question 3"