from app.llm.ollama_client import (
    get_llm,
)

from app.rag.context import (
    format_documents_as_context,
)

from app.rag.prompts import (
    RAG_PROMPT,
)

from app.retrieval.retriever import (
    retrieve_resume_documents,
)


def build_rag_prompt(
    query: str,
    retrieved_context: str | None = None,
    document_id: str | None = None,
    k: int = 4,
):
    """
    Build a RAG prompt.

    Two modes are supported:

    1. Existing-context mode:
       query + retrieved_context

    2. Retrieval mode:
       document_id + query + k

    Retrieval mode returns:
        (prompt, documents)

    Existing-context mode returns:
        prompt
    """

    if not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    if k < 1:
        raise ValueError(
            "k must be greater than 0."
        )

    if document_id is not None:

        if not document_id.strip():
            raise ValueError(
                "document_id cannot be empty."
            )

        documents = retrieve_resume_documents(
            document_id=document_id,
            query=query,
            k=k,
        )

        context = format_documents_as_context(
            documents
        )

        if not context.strip():
            raise ValueError(
                "Retrieved context cannot be empty."
            )

        prompt = RAG_PROMPT.invoke(
            {
                "context": context,
                "question": query,
            }
        )

        return prompt, documents

    if not retrieved_context or not retrieved_context.strip():
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
    retrieved_context: str | None = None,
    document_id: str | None = None,
    k: int = 4,
):
    """
    Generate a grounded answer.

    Existing-context mode returns:

        str

    Retrieval mode returns:

        tuple[str, list]
    """

    if document_id is not None:

        prompt, documents = build_rag_prompt(
            query=query,
            document_id=document_id,
            k=k,
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

        return answer, documents

    prompt = build_rag_prompt(
        query=query,
        retrieved_context=retrieved_context,
        k=k,
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