import re

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


EXPERIENCE_ALIASES = {
    "ml": "machine learning",
    "ai ml": "machine learning",
    "ai/ml": "machine learning",
}


def normalize_experience(
    experience: str,
) -> str:
    """
    Normalize experience text for comparison.
    """

    normalized = " ".join(
        experience.strip().lower().split()
    )

    for alias, canonical in EXPERIENCE_ALIASES.items():
        normalized = re.sub(
            rf"\b{re.escape(alias)}\b",
            canonical,
            normalized,
        )

    return normalized


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


def _is_year_requirement(
    requirement: str,
) -> bool:
    """
    Detect requirements that only express
    a minimum years-of-experience value.
    """

    normalized = normalize_experience(
        requirement
    )

    return bool(
        re.fullmatch(
            r"\d+(?:\.\d+)?\+?",
            normalized,
        )
        or re.fullmatch(
            r"\d+(?:\.\d+)?\+?\s*years?",
            normalized,
        )
    )


def _requirement_is_satisfied(
    requirement: str,
    resume_terms: set[str],
) -> bool:
    """
    Determine whether a job experience
    requirement is supported by the resume.
    """

    if _is_year_requirement(
        requirement
    ):
        # A pure numeric requirement such as
        # "0+" does not provide a meaningful
        # semantic signal for experience matching.
        return True

    requirement_terms = (
        extract_meaningful_terms(
            requirement
        )
    )

    if not requirement_terms:
        return False

    # For multi-word requirements, require
    # all meaningful terms to be represented.
    #
    # Example:
    # "machine learning"
    # must match both "machine" and "learning".
    return requirement_terms.issubset(
        resume_terms
    )


def match_experience(
    resume_experience: list[str],
    job_experience: list[str],
) -> ExperienceMatchResult:
    """
    Match resume experience against
    job experience requirements.

    Matching supports:
    - case-insensitivity
    - whitespace normalization
    - ML -> Machine Learning aliasing
    - semantic term matching
    - numeric year requirements
    """

    if not job_experience:
        return ExperienceMatchResult()

    cleaned_requirements = [
        item.strip()
        for item in job_experience
        if item.strip()
    ]

    if not resume_experience:
        unmatched = [
            item
            for item in cleaned_requirements
            if not _is_year_requirement(item)
        ]

        return ExperienceMatchResult(
            unmatched_experience=unmatched,
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

    for requirement in cleaned_requirements:

        if _requirement_is_satisfied(
            requirement=requirement,
            resume_terms=resume_terms,
        ):
            matched.append(requirement)
        else:
            unmatched.append(requirement)

    return ExperienceMatchResult(
        matched_experience=matched,
        unmatched_experience=unmatched,
    )