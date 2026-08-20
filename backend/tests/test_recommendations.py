from app.job.recommendations import (
    RecommendationResult,
    generate_recommendations,
)


def test_generate_recommendations() -> None:

    result = generate_recommendations(
        matched_skills=[
            "Python",
            "PyTorch",
            "RAG",
        ],
        missing_skills=[
            "AWS",
            "Docker",
            "Kubernetes",
        ],
        matched_experience=[
            "Machine Learning",
        ],
        unmatched_experience=[],
    )

    assert isinstance(
        result,
        RecommendationResult,
    )

    assert result.recommendations

    assert (
        "Highlight your Python, PyTorch, RAG "
        "experience in the resume."
        in result.recommendations
    )

    assert (
        "Add relevant AWS experience if you have it."
        in result.recommendations
    )

    assert (
        "Add relevant Docker experience if you have it."
        in result.recommendations
    )


def test_recommendations_for_unmatched_experience() -> None:

    result = generate_recommendations(
        matched_skills=[
            "Python",
        ],
        missing_skills=[],
        matched_experience=[],
        unmatched_experience=[
            "5+ years of Kubernetes experience",
        ],
    )

    assert result.recommendations

    assert (
        "Strengthen evidence for the requirement: "
        "5+ years of Kubernetes experience"
        in result.recommendations
    )


def test_recommendations_for_perfect_alignment() -> None:

    result = generate_recommendations(
        matched_skills=[
            "Python",
            "PyTorch",
            "RAG",
        ],
        missing_skills=[],
        matched_experience=[
            "Machine Learning experience",
        ],
        unmatched_experience=[],
    )

    assert result.recommendations

    assert (
        "The resume aligns well with the "
        "identified job requirements."
        in result.recommendations
    )


def test_recommendations_for_no_matches() -> None:

    result = generate_recommendations(
        matched_skills=[],
        missing_skills=[],
        matched_experience=[],
        unmatched_experience=[],
    )

    assert result.recommendations

    assert (
        "Review the resume's technical skills "
        "against the job requirements."
        in result.recommendations
    )


def test_recommendations_limit_missing_skills() -> None:

    result = generate_recommendations(
        matched_skills=[],
        missing_skills=[
            "AWS",
            "Docker",
            "Kubernetes",
            "Terraform",
            "Azure",
        ],
        matched_experience=[],
        unmatched_experience=[],
    )

    skill_recommendations = [
        item
        for item in result.recommendations
        if item.startswith("Add relevant")
    ]

    assert len(skill_recommendations) == 3