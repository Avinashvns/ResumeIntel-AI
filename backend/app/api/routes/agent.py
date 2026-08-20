from fastapi import APIRouter, HTTPException

from app.agent.service import (
    ask_resume_agent,
)
from app.schemas.agent import (
    AgentAskRequest,
    AgentAskResponse,
    AgentSource,
)


router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post(
    "/{document_id}/ask",
    response_model=AgentAskResponse,
)
def ask_agent(
    document_id: str,
    request: AgentAskRequest,
) -> AgentAskResponse:

    try:
        result = ask_resume_agent(
            document_id=document_id,
            query=request.query,
            thread_id=request.thread_id,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    sources = [
        AgentSource(
            chunk_id=source["chunk_id"],
            page_number=source["page_number"],
            text=source["text"],
        )
        for source in result["sources"]
    ]

    return AgentAskResponse(
        document_id=result["document_id"],
        query=result["query"],
        answer=result["answer"],
        sources=sources,
        thread_id=result["thread_id"],
    )