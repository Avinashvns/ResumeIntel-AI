from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from app.vectorstore.faiss_store import load_faiss_store


def get_resume_retriever(
    document_id: str,
    k: int = 4,
) -> VectorStoreRetriever:
    """
    Load a resume FAISS index and return
    a LangChain retriever.
    """

    vectorstore = load_faiss_store(
        document_id
    )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
        },
    )


def retrieve_resume_documents(
    document_id: str,
    query: str,
    k: int = 4,
) -> list[Document]:
    """
    Retrieve the most relevant resume documents
    for a user query.
    """

    if not query.strip():
        return []

    retriever = get_resume_retriever(
        document_id=document_id,
        k=k,
    )

    return retriever.invoke(query)