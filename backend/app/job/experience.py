from pydantic import BaseModel, Field


class ExperienceMatchResult(BaseModel):
    """
    Result of matching resume experience
    against job experience requirements.
    """

    matched_experience: list[str] = Field(
        default_factory=list,
    )

    unmatched_experience: list[str] = Field(
        default_factory=list,
    )


STOP_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "from",
    "in",
    "of",
    "on",
    "the",
    "to",
    "with",
    "years",
    "year",
    "experience",
}


def normalize_experience(
    experience: str,
) -> str:
    """
    Normalize experience text for comparison.
    """

    return " ".join(
        experience.strip().lower().split()
    )


def extract_meaningful_terms(
    experience: str,
) -> set[str]:
    """
    Extract meaningful terms from experience text.
    """

    normalized = normalize_experience(
        experience
    )

    return {
        word
        for word in normalized.split()
        if word not in STOP_WORDS
        and word.isalnum()
    }


def match_experience(
    resume_experience: list[str],
    job_experience: list[str],
) -> ExperienceMatchResult:
    """
    Match resume experience against
    job experience requirements.

    Matching is based on shared meaningful
    experience terms while ignoring common
    stop words.
    """

    if not job_experience:
        return ExperienceMatchResult()

    if not resume_experience:
        return ExperienceMatchResult(
            unmatched_experience=[
                item.strip()
                for item in job_experience
                if item.strip()
            ],
        )

    resume_terms: set[str] = set()

    for experience in resume_experience:
        resume_terms.update(
            extract_meaningful_terms(
                experience
            )
        )

    matched: list[str] = []
    unmatched: list[str] = []

    for requirement in job_experience:

        requirement_terms = (
            extract_meaningful_terms(
                requirement
            )
        )

        if not requirement_terms:
            continue

        if requirement_terms & resume_terms:
            matched.append(
                requirement.strip()
            )
        else:
            unmatched.append(
                requirement.strip()
            )

    return ExperienceMatchResult(
        matched_experience=matched,
        unmatched_experience=unmatched,
    )