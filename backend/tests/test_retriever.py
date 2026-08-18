from app.retrieval.retriever import (
    retrieve_resume_documents,
)


DOCUMENT_ID = (
    "2be45ab799dc4d879e7ca430c9650b28"
)


def test_resume_retrieval() -> None:

    query = (
        "Does the candidate have "
        "experience with RAG?"
    )

    documents = retrieve_resume_documents(
        document_id=DOCUMENT_ID,
        query=query,
        k=4,
    )

    assert documents

    print("\nRetrieved documents:")

    for index, document in enumerate(
        documents,
        start=1,
    ):
        print(
            f"\n--- Result {index} ---"
        )

        print(
            "Chunk ID:",
            document.metadata.get(
                "chunk_id"
            ),
        )

        print(
            "Page:",
            document.metadata.get(
                "page_number"
            ),
        )

        print(
            "Text:",
            document.page_content,
        )