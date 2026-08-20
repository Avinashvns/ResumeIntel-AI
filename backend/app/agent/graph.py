from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.agent.state import (
    ResumeAgentState,
)
from app.rag.context import (
    format_documents_as_context,
)
from app.rag.generation_service import (
    generate_grounded_answer,
)
from app.retrieval.retriever import (
    retrieve_resume_documents,
)


def analyze_request(
    state: ResumeAgentState,
) -> ResumeAgentState:
    """
    Validate and normalize the user's resume question.
    """

    query = state["query"].strip()

    if not query:
        raise ValueError(
            "Query cannot be empty."
        )

    return {
        **state,
        "query": query,
    }


def retrieve_context(
    state: ResumeAgentState,
) -> ResumeAgentState:
    """
    Retrieve relevant resume documents using
    the existing semantic retriever.
    """

    documents = retrieve_resume_documents(
        document_id=state["document_id"],
        query=state["query"],
        k=4,
    )

    context = format_documents_as_context(
        documents
    )

    sources = [
        {
            "chunk_id": document.metadata.get(
                "chunk_id",
                "",
            ),
            "page_number": document.metadata.get(
                "page_number",
                "unknown",
            ),
            "text": document.page_content,
        }
        for document in documents
    ]

    return {
        **state,
        "retrieved_context": context,
        "sources": sources,
    }


def generate_answer(
    state: ResumeAgentState,
) -> ResumeAgentState:
    """
    Generate a grounded answer using the existing
    RAG generation pipeline.
    """

    answer, _ = generate_grounded_answer(
        document_id=state["document_id"],
        query=state["query"],
        k=4,
    )

    return {
        **state,
        "answer": answer,
    }


def build_resume_agent():
    """
    Build and compile the ResumeIntel
    LangGraph resume analysis agent.
    """

    workflow = StateGraph(
        ResumeAgentState
    )

    workflow.add_node(
        "analyze_request",
        analyze_request,
    )

    workflow.add_node(
        "retrieve_context",
        retrieve_context,
    )

    workflow.add_node(
        "generate_answer",
        generate_answer,
    )

    workflow.add_edge(
        START,
        "analyze_request",
    )

    workflow.add_edge(
        "analyze_request",
        "retrieve_context",
    )

    workflow.add_edge(
        "retrieve_context",
        "generate_answer",
    )

    workflow.add_edge(
        "generate_answer",
        END,
    )

    return workflow.compile()