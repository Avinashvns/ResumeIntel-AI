from app.rag.generation_service import (
    build_rag_prompt,
)


DOCUMENT_ID = "2be45ab799dc4d879e7ca430c9650b28"


def test_context_injection() -> None:
    query = "Does the candidate have experience with RAG?"

    prompt, documents = build_rag_prompt(
        document_id=DOCUMENT_ID,
        query=query,
        k=4,
    )

    messages = prompt.to_messages()

    assert documents

    assert len(messages) == 2

    system_message = messages[0].content
    human_message = messages[1].content

    assert "resume context" in system_message.lower()

    assert query in human_message

    assert "Source 1" in human_message

    print("\nRetrieved documents:")

    for index, document in enumerate(
        documents,
        start=1,
    ):
        print(f"\n--- Document {index} ---")

        print(
            "Chunk ID:",
            document.metadata.get("chunk_id"),
        )

        print(
            "Page:",
            document.metadata.get("page_number"),
        )

        print(
            "Text:",
            document.page_content,
        )

    print("\nInjected prompt:")

    print(human_message)


def test_context_injection_rejects_empty_query() -> None:
    try:
        build_rag_prompt(
            document_id=DOCUMENT_ID,
            query="",
            k=4,
        )
    except ValueError as exc:
        assert str(exc) == "Query cannot be empty."
    else:
        raise AssertionError("Expected ValueError for empty query.")
