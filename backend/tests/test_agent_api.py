from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


DOCUMENT_ID = (
    "2be45ab799dc4d879e7ca430c9650b28"
)


def test_agent_api() -> None:

    response = client.post(
        f"/api/v1/agent/{DOCUMENT_ID}/ask",
        json={
            "query": (
                "Does the candidate have "
                "experience with ML?"
            ),
            "thread_id": "api-test-session",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["document_id"]
        == DOCUMENT_ID
    )

    assert data["query"]

    assert data["answer"]

    assert isinstance(
        data["answer"],
        str,
    )

    assert data["sources"]

    assert (
        data["thread_id"]
        == "api-test-session"
    )

    print("\nAgent API Answer:")
    print(data["answer"])

    print("\nSources:")

    for source in data["sources"]:
        print(
            f"Page {source['page_number']} "
            f"| {source['chunk_id']}"
        )


def test_agent_api_rejects_empty_query() -> None:

    response = client.post(
        f"/api/v1/agent/{DOCUMENT_ID}/ask",
        json={
            "query": "",
            "thread_id": "api-empty-query-test",
        },
    )

    assert response.status_code == 422