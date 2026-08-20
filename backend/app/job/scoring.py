from pydantic import BaseModel, Field


class MatchScoreResult(BaseModel):
    """
    Transparent resume-to-job match score.
    """

    skill_score: float = Field(
        ge=0,
        le=100,
    )

    experience_score: float = Field(
        ge=0,
        le=100,
    )

    overall_score: float = Field(
        ge=0,
        le=100,
    )


def calculate_match_score(
    total_job_skills: int,
    matched_skills: int,
    total_job_experience: int,
    matched_experience: int,
) -> MatchScoreResult:
    """
    Calculate a transparent resume-to-job
    match score.

    Weights:
    - Skills: 70%
    - Experience: 30%
    """

    if total_job_skills < 0:
        raise ValueError(
            "total_job_skills cannot be negative."
        )

    if matched_skills < 0:
        raise ValueError(
            "matched_skills cannot be negative."
        )

    if total_job_experience < 0:
        raise ValueError(
            "total_job_experience cannot be negative."
        )

    if matched_experience < 0:
        raise ValueError(
            "matched_experience cannot be negative."
        )

    if matched_skills > total_job_skills:
        raise ValueError(
            "matched_skills cannot exceed "
            "total_job_skills."
        )

    if matched_experience > total_job_experience:
        raise ValueError(
            "matched_experience cannot exceed "
            "total_job_experience."
        )

    if total_job_skills == 0:
        skill_score = 0.0
    else:
        skill_score = (
            matched_skills
            / total_job_skills
        ) * 100

    if total_job_experience == 0:
        experience_score = 0.0
    else:
        experience_score = (
            matched_experience
            / total_job_experience
        ) * 100

    overall_score = (
        skill_score * 0.70
        + experience_score * 0.30
    )

    return MatchScoreResult(
        skill_score=round(
            skill_score,
            2,
        ),
        experience_score=round(
            experience_score,
            2,
        ),
        overall_score=round(
            overall_score,
            2,
        ),
    )