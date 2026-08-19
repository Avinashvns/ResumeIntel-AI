from app.llm.ollama_client import get_llm


def test_llm_connection() -> None:
    llm = get_llm()

    response = llm.invoke(
        "Reply with exactly: ResumeIntel AI is working."
    )

    assert response.content

    print("\nLLM response:")
    print(response.content)