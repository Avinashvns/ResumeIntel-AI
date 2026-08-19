from app.rag.prompts import RAG_PROMPT


def test_rag_prompt_variables() -> None:

    prompt_value = RAG_PROMPT.invoke(
        {
            "context": (
                "The candidate has experience "
                "with Python, FastAPI and FAISS."
            ),
            "question": (
                "Does the candidate know FAISS?"
            ),
        }
    )

    messages = prompt_value.to_messages()

    assert len(messages) == 2

    assert (
        "resume context"
        in messages[0].content.lower()
    )

    assert (
        "Does the candidate know FAISS?"
        in messages[1].content
    )


def test_rag_prompt_rejects_missing_context() -> None:

    prompt_value = RAG_PROMPT.invoke(
        {
            "context": "",
            "question": (
                "Does the candidate know Docker?"
            ),
        }
    )

    messages = prompt_value.to_messages()

    assert (
        "Does the candidate know Docker?"
        in messages[1].content
    )