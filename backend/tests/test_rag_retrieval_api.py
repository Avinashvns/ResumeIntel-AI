from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


DOCUMENT_ID = (
    "2be45ab799dc4d879e7ca430c9650b28"
)


def test_rag_retrieval_api() -> None:

    response = client.post(
        f"/api/v1/rag/{DOCUMENT_ID}/retrieve",
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
    assert data["result_count"] > 0
    assert data["results"]

    first_result = data["results"][0]

    assert "chunk_id" in first_result
    assert "text" in first_result
    assert "metadata" in first_result