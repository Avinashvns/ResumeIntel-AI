from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.embeddings.model import (
    get_embedding_model,
)


VECTORSTORE_DIR = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "vectorstore"
)


def create_faiss_store(
    documents: list[Document],
) -> FAISS:
    """
    Create a FAISS vector store from LangChain Documents.
    """

    if not documents:
        raise ValueError(
            "Cannot create FAISS store from empty documents."
        )

    embedding_model = get_embedding_model()

    return FAISS.from_documents(
        documents=documents,
        embedding=embedding_model,
    )


def save_faiss_store(
    vectorstore: FAISS,
    index_name: str,
) -> Path:
    """
    Persist FAISS vector store locally.
    """

    index_directory = VECTORSTORE_DIR / index_name

    index_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    vectorstore.save_local(
        str(index_directory)
    )

    return index_directory


def load_faiss_store(
    index_name: str,
) -> FAISS:
    """
    Load a persisted FAISS vector store.
    """

    index_directory = (
        VECTORSTORE_DIR / index_name
    )

    if not index_directory.exists():
        raise FileNotFoundError(
            f"FAISS index not found: {index_directory}"
        )

    embedding_model = get_embedding_model()

    return FAISS.load_local(
        str(index_directory),
        embedding_model,
        allow_dangerous_deserialization=True,
    )