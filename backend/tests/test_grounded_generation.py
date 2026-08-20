from app.rag.generation_service import (
    build_rag_prompt,
    generate_grounded_answer,
)


RETRIEVED_CONTEXT = """
[Source 1]
Chunk ID: page-1-chunk-3
Page: 1
Content:
AI/ML Engineer with experience in building
and deploying end-to-end machine learning
applications.

[Source 2]
Chunk ID: page-1-chunk-4
Page: 1
Content:
TECHNICAL SKILLS:
Machine Learning, Scikit-learn,
NumPy, Pandas, Flask, AWS, Docker.
"""


def test_rag_prompt_uses_retrieved_context() -> None:

    query = (
        "Does the candidate have "
        "experience with ML?"
    )

    prompt = build_rag_prompt(
        query=query,
        retrieved_context=RETRIEVED_CONTEXT,
    )

    assert prompt

    prompt_text = str(prompt)

    assert "AI/ML Engineer" in prompt_text

    assert "Machine Learning" in prompt_text

    print("\nRAG Prompt:")
    print(prompt_text)


def test_grounded_answer_generation() -> None:

    query = (
        "Does the candidate have "
        "experience with ML?"
    )

    answer = generate_grounded_answer(
        query=query,
        retrieved_context=RETRIEVED_CONTEXT,
    )

    assert answer

    assert isinstance(
        answer,
        str,
    )

    print("\nGenerated answer:")
    print(answer)


def test_grounded_answer_rejects_empty_query() -> None:

    try:
        generate_grounded_answer(
            query="",
            retrieved_context=RETRIEVED_CONTEXT,
        )

    except ValueError as exc:

        assert str(exc) == (
            "Query cannot be empty."
        )

    else:

        raise AssertionError(
            "Expected ValueError for empty query."
        )


def test_grounded_answer_rejects_empty_context() -> None:

    query = (
        "Does the candidate have "
        "experience with ML?"
    )

    try:
        generate_grounded_answer(
            query=query,
            retrieved_context="",
        )

    except ValueError as exc:

        assert str(exc) == (
            "Retrieved context cannot be empty."
        )

    else:

        raise AssertionError(
            "Expected ValueError for empty context."
        )