from fastapi.testclient import (
    TestClient,
)

from main import app


client = TestClient(app)


def test_analyze_requires_stored_filename():
    response = client.post(
        "/api/v1/analyze",
        json={
            "stored_filename": "",
            "job_description": (
                "Python ML Engineer"
            ),
        },
    )

    assert response.status_code == 422


def test_analyze_requires_job_description():
    response = client.post(
        "/api/v1/analyze",
        json={
            "stored_filename": "resume.pdf",
            "job_description": "",
        },
    )

    assert response.status_code == 422