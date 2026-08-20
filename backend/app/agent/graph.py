from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.agent.state import (
    ResumeAgentState,
)
from app.agent.tools import (
    search_resume,
)
from app.rag.generation_service import (
    generate_grounded_answer,
)

from langgraph.checkpoint.memory import (
    MemorySaver,
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
    Use the resume search tool to retrieve
    relevant resume information.
    """

    result = search_resume.invoke(
        {
            "document_id": state["document_id"],
            "query": state["query"],
            "k": 4,
        }
    )

    return {
        **state,
        "retrieved_context": result,
    }


def generate_answer(
    state: ResumeAgentState,
) -> ResumeAgentState:
    """
    Generate the final grounded answer.
    """

    answer, documents = generate_grounded_answer(
        document_id=state["document_id"],
        query=state["query"],
        k=4,
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
        "answer": answer,
        "sources": sources,
    }


def build_resume_agent():
    """
    Build the ResumeIntel LangGraph agent
    with short-term conversation memory.
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

    checkpointer = MemorySaver()

    return workflow.compile(
        checkpointer=checkpointer,
    )