from app.rag.generation_service import (
    generate_grounded_answer,
)


DOCUMENT_ID = "2be45ab799dc4d879e7ca430c9650b28"


def test_grounded_answer_generation() -> None:
    query = "Does the candidate have experience with RAG?"

    answer, documents = generate_grounded_answer(
        document_id=DOCUMENT_ID,
        query=query,
        k=4,
    )

    assert answer
    assert isinstance(answer, str)

    assert documents

    print("\nGenerated answer:")
    print(answer)

    print("\nSources:")

    for document in documents:
        print(
            "Chunk:",
            document.metadata.get("chunk_id"),
            "| Page:",
            document.metadata.get("page_number"),
        )


def test_grounded_answer_rejects_empty_query() -> None:
    try:
        generate_grounded_answer(
            document_id=DOCUMENT_ID,
            query="",
            k=4,
        )
    except ValueError as exc:
        assert str(exc) == "Query cannot be empty."
    else:
        raise AssertionError("Expected ValueError for empty query.")


def test_grounded_answer_handles_missing_information() -> None:
    query = "Does the candidate have professional experience flying aircraft?"

    answer, documents = generate_grounded_answer(
        document_id=DOCUMENT_ID,
        query=query,
        k=4,
    )

    assert answer
    assert documents

    print("\nMissing-information answer:")
    print(answer)
