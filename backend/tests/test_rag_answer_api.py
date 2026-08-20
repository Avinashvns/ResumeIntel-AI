from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


DOCUMENT_ID = (
    "2be45ab799dc4d879e7ca430c9650b28"
)


def test_rag_answer_api() -> None:

    response = client.post(
        f"/api/v1/rag/{DOCUMENT_ID}/ask",
        json={
            "query": (
                "Does the candidate have "
                "experience with RAG?"
            ),
            "k": 4,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_id"] == DOCUMENT_ID
    assert data["query"]
    assert data["answer"]
    assert isinstance(
        data["answer"],
        str,
    )

    assert data["sources"]

    first_source = data["sources"][0]

    assert "chunk_id" in first_source
    assert "page_number" in first_source
    assert "text" in first_source

    print("\nAnswer:")
    print(data["answer"])

    print("\nSources:")

    for source in data["sources"]:
        print(
            f"Page {source['page_number']} "
            f"| {source['chunk_id']}"
        )


def test_rag_answer_api_rejects_empty_query() -> None:

    response = client.post(
        f"/api/v1/rag/{DOCUMENT_ID}/ask",
        json={
            "query": "",
            "k": 4,
        },
    )

    assert response.status_code == 422