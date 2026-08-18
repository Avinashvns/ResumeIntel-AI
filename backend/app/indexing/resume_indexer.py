from pathlib import Path

from langchain_core.documents import Document

from app.ingestion.chunker import chunk_text
from app.ingestion.document_builder import (
    build_resume_document,
)
from app.ingestion.pdf_extractor import (
    extract_pdf_text,
)
from app.ingestion.text_cleaner import clean_text
from app.vectorstore.faiss_store import (
    create_faiss_store,
    save_faiss_store,
)


def build_resume_documents(
    file_path: Path,
    document_id: str,
    filename: str,
) -> list[Document]:
    """
    Build LangChain Documents from a resume PDF.
    """

    pages = extract_pdf_text(file_path)

    documents: list[Document] = []

    for page in pages:
        cleaned_text = clean_text(
            page["text"]
        )

        chunks = chunk_text(
            cleaned_text
        )

        for index, text_chunk in enumerate(
            chunks,
            start=1,
        ):
            chunk_id = (
                f"page-{page['page_number']}"
                f"-chunk-{index}"
            )

            document = build_resume_document(
                text=text_chunk,
                document_id=document_id,
                filename=filename,
                page_number=page["page_number"],
                chunk_id=chunk_id,
            )

            documents.append(document)

    return documents


def index_resume(
    file_path: Path,
    document_id: str,
    filename: str,
) -> tuple[int, Path]:

    documents = build_resume_documents(
        file_path=file_path,
        document_id=document_id,
        filename=filename,
    )

    if not documents:
        raise ValueError(
            "No indexable text found in resume."
        )

    vectorstore = create_faiss_store(
        documents
    )

    index_path = save_faiss_store(
        vectorstore,
        document_id,
    )

    return len(documents), index_path