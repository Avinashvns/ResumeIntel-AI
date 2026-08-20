from pydantic import BaseModel, Field


class RecommendationResult(BaseModel):
    """
    Recommendations generated from resume-job
    comparison results.
    """

    recommendations: list[str] = Field(
        default_factory=list,
    )


def generate_recommendations(
    matched_skills: list[str],
    missing_skills: list[str],
    matched_experience: list[str],
    unmatched_experience: list[str],
) -> RecommendationResult:
    """
    Generate transparent recommendations from
    existing resume-job analysis results.
    """

    recommendations: list[str] = []

    if matched_skills:
        recommendations.append(
            "Highlight your "
            + ", ".join(matched_skills[:3])
            + " experience in the resume."
        )

    for skill in missing_skills[:3]:
        recommendations.append(
            f"Add relevant {skill} experience "
            "if you have it."
        )

    for experience in unmatched_experience[:2]:
        recommendations.append(
            "Strengthen evidence for the "
            f"requirement: {experience}"
        )

    if not matched_skills:
        recommendations.append(
            "Review the resume's technical skills "
            "against the job requirements."
        )

    if (
        not missing_skills
        and not unmatched_experience
    ):
        recommendations.append(
            "The resume aligns well with the "
            "identified job requirements."
        )

    return RecommendationResult(
        recommendations=recommendations,
    )