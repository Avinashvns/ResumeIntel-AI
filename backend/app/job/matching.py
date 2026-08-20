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
    but not found in the resume skills.
    """

    missing_skills: list[str] = Field(
        default_factory=list,
    )


SKILL_ALIASES = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "genai": "generative ai",
    "gen ai": "generative ai",
    "llm": "large language model",
    "llms": "large language model",
}


def normalize_skill(
    skill: str,
) -> str:
    """
    Normalize a skill for reliable comparison.
    """

    normalized = " ".join(skill.strip().lower().split())

    return SKILL_ALIASES.get(
        normalized,
        normalized,
    )


def _deduplicate_skills(
    skills: list[str],
) -> list[str]:
    """
    Remove semantically duplicate skills
    while preserving the first representation.
    """

    result: list[str] = []
    seen: set[str] = set()

    for skill in skills:
        if not skill.strip():
            continue

        normalized = normalize_skill(skill)

        if normalized in seen:
            continue

        seen.add(normalized)
        result.append(skill.strip())

    return result


def merge_job_skills(
    skills: list[str],
    tools: list[str],
) -> list[str]:
    """
    Combine job skills and tools into one
    canonical matching requirement list.
    """

    return _deduplicate_skills(
        [
            *skills,
            *tools,
        ]
    )


def match_skills(
    resume_skills: list[str],
    job_skills: list[str],
) -> SkillMatchResult:
    """
    Match resume skills against job skills.

    Matching supports:
    - case-insensitivity
    - whitespace normalization
    - common skill aliases
    - semantic duplicate removal
    """

    if not resume_skills or not job_skills:
        return SkillMatchResult()

    resume_skill_map = {
        normalize_skill(skill): skill.strip()
        for skill in resume_skills
        if skill.strip()
    }

    unique_job_skills = _deduplicate_skills(job_skills)

    matched_skills: list[str] = []

    for job_skill in unique_job_skills:
        normalized_job_skill = normalize_skill(job_skill)

        if normalized_job_skill in resume_skill_map:
            matched_skills.append(resume_skill_map[normalized_job_skill])

    return SkillMatchResult(
        matched_skills=matched_skills,
    )


def find_missing_skills(
    resume_skills: list[str],
    job_skills: list[str],
) -> MissingSkillResult:
    """
    Find unique job skills that are not present
    in the resume.
    """

    if not job_skills:
        return MissingSkillResult()

    resume_skill_set = {
        normalize_skill(skill) for skill in resume_skills if skill.strip()
    }

    unique_job_skills = _deduplicate_skills(job_skills)

    missing_skills: list[str] = []

    for job_skill in unique_job_skills:
        normalized_job_skill = normalize_skill(job_skill)

        if normalized_job_skill and normalized_job_skill not in resume_skill_set:
            missing_skills.append(job_skill.strip())

    return MissingSkillResult(
        missing_skills=missing_skills,
    )
