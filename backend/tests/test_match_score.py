import pytest

from app.job.scoring import (
    MatchScoreResult,
    calculate_match_score,
)


def test_match_score() -> None:

    result = calculate_match_score(
        total_job_skills=5,
        matched_skills=4,
        total_job_experience=2,
        matched_experience=1,
    )

    assert isinstance(
        result,
        MatchScoreResult,
    )

    assert result.skill_score == 80.0

    assert result.experience_score == 50.0

    assert result.overall_score == 71.0


def test_perfect_match() -> None:

    result = calculate_match_score(
        total_job_skills=5,
        matched_skills=5,
        total_job_experience=2,
        matched_experience=2,
    )

    assert result.skill_score == 100.0

    assert result.experience_score == 100.0

    assert result.overall_score == 100.0


def test_no_match() -> None:

    result = calculate_match_score(
        total_job_skills=5,
        matched_skills=0,
        total_job_experience=2,
        matched_experience=0,
    )

    assert result.skill_score == 0.0

    assert result.experience_score == 0.0

    assert result.overall_score == 0.0


def test_zero_experience_requirements() -> None:

    result = calculate_match_score(
        total_job_skills=4,
        matched_skills=2,
        total_job_experience=0,
        matched_experience=0,
    )

    assert result.skill_score == 50.0

    assert result.experience_score == 0.0

    assert result.overall_score == 35.0


def test_invalid_skill_match() -> None:

    with pytest.raises(
        ValueError,
        match="matched_skills cannot exceed",
    ):
        calculate_match_score(
            total_job_skills=3,
            matched_skills=4,
            total_job_experience=1,
            matched_experience=1,
        )


def test_invalid_experience_match() -> None:

    with pytest.raises(
        ValueError,
        match="matched_experience cannot exceed",
    ):
        calculate_match_score(
            total_job_skills=3,
            matched_skills=2,
            total_job_experience=1,
            matched_experience=2,
        )