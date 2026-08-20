from app.job.experience import (
    ExperienceMatchResult,
    match_experience,
)


def test_experience_matching() -> None:

    resume_experience = [
        "AI/ML Engineer with experience "
        "in building machine learning applications.",
    ]

    job_experience = [
        "2+ years of experience in machine learning",
    ]

    result = match_experience(
        resume_experience=resume_experience,
        job_experience=job_experience,
    )

    assert isinstance(
        result,
        ExperienceMatchResult,
    )

    assert result.matched_experience == [
        "2+ years of experience in machine learning"
    ]

    assert result.unmatched_experience == []


def test_experience_matching_detects_unmatched() -> None:

    resume_experience = [
        "AI/ML Engineer with experience "
        "in building machine learning applications.",
    ]

    job_experience = [
        "Experience in machine learning",
        "Experience in Kubernetes",
    ]

    result = match_experience(
        resume_experience=resume_experience,
        job_experience=job_experience,
    )

    assert (
        "Experience in machine learning"
        in result.matched_experience
    )

    assert (
        "Experience in Kubernetes"
        in result.unmatched_experience
    )


def test_experience_matching_handles_empty_resume() -> None:

    result = match_experience(
        resume_experience=[],
        job_experience=[
            "Experience in machine learning",
        ],
    )

    assert result.matched_experience == []

    assert result.unmatched_experience == [
        "Experience in machine learning"
    ]


def test_experience_matching_handles_empty_job() -> None:

    result = match_experience(
        resume_experience=[
            "Machine Learning Engineer",
        ],
        job_experience=[],
    )

    assert result.matched_experience == []

    assert result.unmatched_experience == []