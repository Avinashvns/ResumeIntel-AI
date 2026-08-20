from app.job.matching import (
    MissingSkillResult,
    SkillMatchResult,
    find_missing_skills,
    match_skills,
)


def test_skill_matching() -> None:
    """
    Resume and JD skills should be matched correctly.
    """

    resume_skills = [
        "Python",
        "PyTorch",
        "RAG",
        "FastAPI",
    ]

    job_skills = [
        "Python",
        "PyTorch",
        "RAG",
        "LangChain",
    ]

    result = match_skills(
        resume_skills=resume_skills,
        job_skills=job_skills,
    )

    assert isinstance(
        result,
        SkillMatchResult,
    )

    assert result.matched_skills == [
        "Python",
        "PyTorch",
        "RAG",
    ]


def test_skill_matching_is_case_insensitive() -> None:
    """
    Skill matching should ignore letter case.
    """

    result = match_skills(
        resume_skills=[
            "python",
            "pytorch",
        ],
        job_skills=[
            "Python",
            "PyTorch",
        ],
    )

    assert result.matched_skills == [
        "python",
        "pytorch",
    ]


def test_skill_matching_normalizes_whitespace() -> None:
    """
    Extra whitespace should not affect matching.
    """

    result = match_skills(
        resume_skills=[
            "Machine Learning",
        ],
        job_skills=[
            "  machine   learning  ",
        ],
    )

    assert result.matched_skills == [
        "Machine Learning",
    ]


def test_skill_matching_handles_empty_resume() -> None:
    """
    Empty resume skills should produce no matches.
    """

    result = match_skills(
        resume_skills=[],
        job_skills=[
            "Python",
        ],
    )

    assert result.matched_skills == []


def test_skill_matching_handles_empty_job_skills() -> None:
    """
    Empty job skills should produce no matches.
    """

    result = match_skills(
        resume_skills=[
            "Python",
        ],
        job_skills=[],
    )

    assert result.matched_skills == []


def test_missing_skill_detection() -> None:
    """
    Skills required by the job but absent
    from the resume should be detected.
    """

    resume_skills = [
        "Python",
        "PyTorch",
        "RAG",
        "FastAPI",
    ]

    job_skills = [
        "Python",
        "PyTorch",
        "RAG",
        "LangChain",
        "AWS",
    ]

    result = find_missing_skills(
        resume_skills=resume_skills,
        job_skills=job_skills,
    )

    assert isinstance(
        result,
        MissingSkillResult,
    )

    assert result.missing_skills == [
        "LangChain",
        "AWS",
    ]


def test_missing_skill_detection_is_case_insensitive() -> None:
    """
    Missing skill detection should ignore case.
    """

    result = find_missing_skills(
        resume_skills=[
            "python",
            "pytorch",
        ],
        job_skills=[
            "Python",
            "PyTorch",
            "RAG",
        ],
    )

    assert result.missing_skills == [
        "RAG",
    ]


def test_missing_skill_detection_normalizes_whitespace() -> None:
    """
    Extra whitespace should not create
    a false missing skill.
    """

    result = find_missing_skills(
        resume_skills=[
            "Machine Learning",
        ],
        job_skills=[
            "machine   learning",
            "PyTorch",
        ],
    )

    assert result.missing_skills == [
        "PyTorch",
    ]


def test_missing_skill_detection_empty_job() -> None:
    """
    Empty job skills should produce no
    missing skills.
    """

    result = find_missing_skills(
        resume_skills=[
            "Python",
        ],
        job_skills=[],
    )

    assert result.missing_skills == []