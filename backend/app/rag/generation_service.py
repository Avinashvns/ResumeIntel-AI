from app.llm.ollama_client import get_llm
from app.rag.context import (
    format_documents_as_context,
)
from app.rag.prompts import RAG_PROMPT
from app.retrieval.retriever import (
    retrieve_resume_documents,
)


def build_rag_prompt(
    document_id: str,
    query: str,
    k: int = 4,
):
    """
    Retrieve relevant resume documents and inject
    them into the RAG prompt.
    """

    if not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    if k < 1:
        raise ValueError(
            "k must be greater than 0."
        )

    documents = retrieve_resume_documents(
        document_id=document_id,
        query=query,
        k=k,
    )

    context = format_documents_as_context(
        documents
    )

    prompt = RAG_PROMPT.invoke(
        {
            "context": context,
            "question": query,
        }
    )

    return prompt, documents


def generate_grounded_answer(
    document_id: str,
    query: str,
    k: int = 4,
) -> tuple[str, list]:
    """
    Retrieve relevant resume context and generate
    a grounded answer using the configured LLM.
    """

    prompt, documents = build_rag_prompt(
        document_id=document_id,
        query=query,
        k=k,
    )

    llm = get_llm()

    response = llm.invoke(prompt)

    answer = response.content.strip()

    if not answer:
        raise ValueError(
            "LLM returned an empty answer."
        )

    return answer, documents