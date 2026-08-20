from app.agent.graph import build_resume_agent


_agent = build_resume_agent()


def ask_resume_agent(
    document_id: str,
    query: str,
    thread_id: str,
) -> dict:
    """
    Execute the ResumeIntel LangGraph agent.
    """

    if not document_id.strip():
        raise ValueError(
            "document_id cannot be empty."
        )

    if not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    if not thread_id.strip():
        raise ValueError(
            "thread_id cannot be empty."
        )

    result = _agent.invoke(
        {
            "document_id": document_id,
            "query": query,
            "retrieved_context": "",
            "answer": "",
            "sources": [],
            "messages": [],
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    return {
        "document_id": result["document_id"],
        "query": result["query"],
        "answer": result["answer"],
        "sources": result["sources"],
        "thread_id": thread_id,
    }