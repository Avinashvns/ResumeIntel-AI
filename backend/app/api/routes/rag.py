from fastapi import APIRouter, HTTPException

from app.rag.retrieval_service import (
    retrieve_resume_context,
)
from app.rag.generation_service import (
    generate_grounded_answer,
)
from app.schemas.rag import (
    RAGAnswerRequest,
    RAGAnswerResponse,
    RAGRetrievedDocument,
    RAGRetrievalRequest,
    RAGRetrievalResponse,
    RAGSource,
)


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post(
    "/{document_id}/retrieve",
    response_model=RAGRetrievalResponse,
)
def retrieve_context(
    document_id: str,
    request: RAGRetrievalRequest,
) -> RAGRetrievalResponse:

    try:
        documents = retrieve_resume_context(
            document_id=document_id,
            query=request.query,
            k=request.k,
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

    results = [
        RAGRetrievedDocument(
            chunk_id=document.metadata.get(
                "chunk_id",
                "",
            ),
            text=document.page_content,
            metadata=document.metadata,
        )
        for document in documents
    ]

    return RAGRetrievalResponse(
        document_id=document_id,
        query=request.query,
        result_count=len(results),
        results=results,
    )


@router.post(
    "/{document_id}/ask",
    response_model=RAGAnswerResponse,
)
def ask_resume(
    document_id: str,
    request: RAGAnswerRequest,
) -> RAGAnswerResponse:

    try:
        answer, documents = (
            generate_grounded_answer(
                document_id=document_id,
                query=request.query,
                k=request.k,
            )
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
        RAGSource(
            chunk_id=document.metadata.get(
                "chunk_id",
                "",
            ),
            page_number=document.metadata.get(
                "page_number",
                "unknown",
            ),
            text=document.page_content,
        )
        for document in documents
    ]

    return RAGAnswerResponse(
        document_id=document_id,
        query=request.query,
        answer=answer,
        sources=sources,
    )