from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.agent.state import (
    ResumeAgentState,
)


def analyze_request(
    state: ResumeAgentState,
) -> ResumeAgentState:
    """
    Initial agent node.

    Validates and prepares the user request.
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
    Placeholder retrieval node.

    The actual resume retrieval tool will be
    connected in Feature 23.
    """

    return {
        **state,
        "retrieved_context": "",
    }


def generate_answer(
    state: ResumeAgentState,
) -> ResumeAgentState:
    """
    Placeholder answer generation node.

    The existing RAG generation service will be
    connected through the agent in later features.
    """

    return {
        **state,
        "answer": "",
    }


def build_resume_agent():
    """
    Build the ResumeIntel LangGraph workflow.
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