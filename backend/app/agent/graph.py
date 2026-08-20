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


async def retrieve_context(
    state: ResumeAgentState,
) -> ResumeAgentState:
    """
    Use the MCP-backed resume search tool
    to retrieve relevant resume information.
    """

    result = await search_resume.ainvoke(
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
    Generate the final grounded answer using
    the context already retrieved through MCP.
    """

    answer = generate_grounded_answer(
        query=state["query"],
        retrieved_context=state["retrieved_context"],
    )

    sources: list[dict] = []

    context = state["retrieved_context"]

    blocks = context.split("[Source ")

    for block in blocks[1:]:
        lines = block.splitlines()

        if not lines:
            continue

        source_number = lines[0].rstrip("]")

        chunk_id = ""

        page_number = "unknown"

        content_lines: list[str] = []

        for line in lines[1:]:

            if line.startswith("Chunk ID:"):
                chunk_id = line.replace(
                    "Chunk ID:",
                    "",
                    1,
                ).strip()

            elif line.startswith("Page:"):
                page_number = line.replace(
                    "Page:",
                    "",
                    1,
                ).strip()

            elif line.startswith("Content:"):
                continue

            else:
                content_lines.append(line)

        sources.append(
            {
                "source": source_number,
                "chunk_id": chunk_id,
                "page_number": page_number,
                "text": "\n".join(
                    content_lines
                ).strip(),
            }
        )

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