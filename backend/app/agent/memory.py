from langchain_core.messages import (
    BaseMessage,
)


def get_recent_messages(
    messages: list[BaseMessage],
    limit: int = 6,
) -> list[BaseMessage]:
    """
    Return the most recent conversation messages.
    """

    if limit < 1:
        raise ValueError(
            "limit must be greater than 0."
        )

    return messages[-limit:]