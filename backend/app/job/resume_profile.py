import re

from pydantic import BaseModel, Field

from app.ingestion.pdf_extractor import (
    PDFExtractionError,
    extract_pdf_text,
)
from app.ingestion.storage import (
    get_resume_path,
)
from app.ingestion.text_cleaner import (
    clean_text,
)
from app.llm.ollama_client import (
    get_llm,
)


class ResumeProfile(BaseModel):
    """
    Structured information extracted from
    an uploaded resume.
    """

    skills: list[str] = Field(
        default_factory=list,
    )

    experience: list[str] = Field(
        default_factory=list,
    )


RESUME_EXPERIENCE_PROMPT = """
You are a strict resume experience extraction system.

Extract ONLY professional and project experience
explicitly present in the resume.

Return ONLY:

experience

Rules:

1. Do not invent companies, job titles, dates,
   responsibilities, or technologies.
2. Do not return education.
3. Do not return certifications.
4. Keep each experience item meaningful and concise.
5. Preserve technical details when they are part
   of the experience statement.
6. Return [] if no experience is present.

Resume:

{resume_text}
"""


SKILL_SECTION_HEADERS = (
    "technical skills",
    "technical skill",
    "skills",
)


def _normalize_skill(
    skill: str,
) -> str | None:
    """
    Normalize one extracted resume skill.
    """

    value = skill.strip()

    if not value:
        return None

    value = re.sub(
        r"^[•\-*]\s*",
        "",
        value,
    )

    if ":" in value:
        value = value.split(
            ":",
            1,
        )[1].strip()

    if not value:
        return None

    return value


def _normalize_skills(
    skills: list[str],
) -> list[str]:
    """
    Normalize and deduplicate skills.
    """

    normalized: list[str] = []
    seen: set[str] = set()

    for skill in skills:
        clean_skill = _normalize_skill(
            skill
        )

        if not clean_skill:
            continue

        key = clean_skill.casefold()

        if key in seen:
            continue

        seen.add(key)
        normalized.append(clean_skill)

    return normalized


def _normalize_experience(
    experience: list[str],
) -> list[str]:
    """
    Normalize and deduplicate experience.
    """

    normalized: list[str] = []
    seen: set[str] = set()

    for item in experience:
        value = item.strip()

        if not value:
            continue

        key = value.casefold()

        if key in seen:
            continue

        seen.add(key)
        normalized.append(value)

    return normalized


def _extract_skill_section(
    resume_text: str,
) -> list[str]:
    """
    Extract explicit skills from the technical
    skills section of the resume.
    """

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    skills: list[str] = []

    inside_skill_section = False

    for line in lines:
        lowered = line.casefold()

        if any(
            header in lowered
            for header in SKILL_SECTION_HEADERS
        ):
            inside_skill_section = True
            continue

        if not inside_skill_section:
            continue

        if lowered in {
            "experience",
            "work experience",
            "professional experience",
            "projects",
            "education",
            "certifications",
        }:
            break

        if ":" in line:
            _, values = line.split(
                ":",
                1,
            )

            skills.extend(
                part.strip()
                for part in values.split(",")
                if part.strip()
            )

    return _normalize_skills(
        skills
    )


def _extract_experience(
    resume_text: str,
) -> list[str]:
    """
    Extract experience using the existing LLM.
    """

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        ResumeProfile
    )

    prompt = RESUME_EXPERIENCE_PROMPT.format(
        resume_text=resume_text,
    )

    result = structured_llm.invoke(
        prompt
    )

    if not isinstance(
        result,
        ResumeProfile,
    ):
        raise ValueError(
            "Failed to extract resume experience."
        )

    return _normalize_experience(
        result.experience
    )


def extract_resume_profile(
    stored_filename: str,
) -> ResumeProfile:
    """
    Extract a structured resume profile.
    """

    if not stored_filename.strip():
        raise ValueError(
            "stored_filename cannot be empty."
        )

    file_path = get_resume_path(
        stored_filename
    )

    if not file_path.exists():
        raise FileNotFoundError(
            "Resume file not found."
        )

    try:
        pages = extract_pdf_text(
            file_path
        )
    except PDFExtractionError as exc:
        raise ValueError(
            str(exc)
        ) from exc

    resume_text = "\n\n".join(
        clean_text(page["text"])
        for page in pages
        if page["text"].strip()
    ).strip()

    if not resume_text:
        raise ValueError(
            "Resume does not contain readable text."
        )

    skills = _extract_skill_section(
        resume_text
    )

    experience = _extract_experience(
        resume_text
    )

    return ResumeProfile(
        skills=skills,
        experience=experience,
    )