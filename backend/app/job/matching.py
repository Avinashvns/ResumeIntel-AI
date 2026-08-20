from pydantic import BaseModel, Field


class SkillMatchResult(BaseModel):
    """
    Result of matching resume skills
    against job description skills.
    """

    matched_skills: list[str] = Field(
        default_factory=list,
    )


class MissingSkillResult(BaseModel):
    """
    Skills required by the job description
    but not found in the resume.
    """

    missing_skills: list[str] = Field(
        default_factory=list,
    )


def normalize_skill(
    skill: str,
) -> str:
    """
    Normalize a skill for reliable comparison.
    """

    return " ".join(
        skill.strip().lower().split()
    )


def match_skills(
    resume_skills: list[str],
    job_skills: list[str],
) -> SkillMatchResult:
    """
    Match resume skills against job skills.

    Matching is:
    - case-insensitive
    - whitespace-normalized
    """

    if not resume_skills:
        return SkillMatchResult()

    if not job_skills:
        return SkillMatchResult()

    resume_skill_map = {
        normalize_skill(skill): skill
        for skill in resume_skills
        if skill.strip()
    }

    matched_skills: list[str] = []

    for job_skill in job_skills:

        normalized_job_skill = normalize_skill(
            job_skill
        )

        if normalized_job_skill in resume_skill_map:
            matched_skills.append(
                resume_skill_map[
                    normalized_job_skill
                ]
            )

    return SkillMatchResult(
        matched_skills=matched_skills,
    )


def find_missing_skills(
    resume_skills: list[str],
    job_skills: list[str],
) -> MissingSkillResult:
    """
    Find job skills that are not present
    in the resume skills.
    """

    if not job_skills:
        return MissingSkillResult()

    resume_skill_set = {
        normalize_skill(skill)
        for skill in resume_skills
        if skill.strip()
    }

    missing_skills: list[str] = []

    for job_skill in job_skills:

        normalized_job_skill = normalize_skill(
            job_skill
        )

        if (
            normalized_job_skill
            and normalized_job_skill
            not in resume_skill_set
        ):
            missing_skills.append(
                job_skill.strip()
            )

    return MissingSkillResult(
        missing_skills=missing_skills,
    )