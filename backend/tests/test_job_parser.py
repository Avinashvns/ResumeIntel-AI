import pytest

from app.job.parser import (
    parse_job_description,
)

from app.job.schemas import (
    JobRequirements,
)


JOB_DESCRIPTION = """
We are looking for an AI/ML Engineer.

Requirements:
- 2+ years of experience in machine learning.
- Strong Python and PyTorch skills.
- Experience with LangChain, RAG and FastAPI.
- Knowledge of AWS and Docker.
- Bachelor's or Master's degree in Computer Science.

Responsibilities:
- Build and deploy machine learning applications.
- Develop RAG-based AI systems.
- Build production APIs.
"""


def test_parse_job_description() -> None:

    result = parse_job_description(
        JOB_DESCRIPTION
    )

    assert isinstance(
        result,
        JobRequirements,
    )

    assert result.skills

    assert result.experience

    assert result.education

    assert result.tools

    assert result.responsibilities

    print("\nParsed Job Requirements:")
    print(result.model_dump())


def test_parse_job_description_rejects_empty_input() -> None:

    with pytest.raises(
        ValueError,
        match="Job description cannot be empty.",
    ):
        parse_job_description("")