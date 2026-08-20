from app.llm.ollama_client import get_llm

from app.rag.prompts import (
    RAG_PROMPT,
)


def build_rag_prompt(
    query: str,
    retrieved_context: str,
):
    """
    Build the RAG prompt using already retrieved
    resume context.

    Retrieval is intentionally not performed here.
    """

    if not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    if not retrieved_context.strip():
        raise ValueError(
            "Retrieved context cannot be empty."
        )

    prompt = RAG_PROMPT.invoke(
        {
            "context": retrieved_context,
            "question": query,
        }
    )

    return prompt


def generate_grounded_answer(
    query: str,
    retrieved_context: str,
) -> str:
    """
    Generate a grounded answer using the
    already retrieved resume context.
    """

    prompt = build_rag_prompt(
        query=query,
        retrieved_context=retrieved_context,
    )

    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    answer = response.content.strip()

    if not answer:
        raise ValueError(
            "LLM returned an empty answer."
        )

    return answer