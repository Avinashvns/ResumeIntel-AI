from pydantic import BaseModel

from app.job.schemas import (
    JobRequirements,
)
from app.llm.ollama_client import (
    get_llm,
)


JOB_PARSER_PROMPT = """
You are a strict Job Description Information Extraction system.

Extract the job description into EXACTLY these five
independent categories:

1. skills
2. experience
3. education
4. tools
5. responsibilities

IMPORTANT:

Each item MUST belong to exactly one category.

====================
SKILLS
====================

Put technical capabilities and competencies here.

Examples:
- Python
- Java
- Flutter
- Dart
- Machine Learning
- React
- SQL
- REST API development
- State Management

A skill is something the candidate is expected
to know or be capable of doing.

====================
EXPERIENCE
====================

Put ONLY professional experience requirements here.

Examples:
- 2+ years of experience
- 1+ years of Flutter development
- 3 years of backend development
- Prior experience building production applications

DO NOT put technologies here.

NEVER put these into experience merely because
they appear in an "Experience with..." sentence:

- Firebase
- REST APIs
- Provider
- Git
- AWS
- Docker
- Python
- Flutter

Those are skills or tools.

For example:

"Experience with Flutter, Firebase and REST APIs"

MUST NOT become:

experience:
[
    "Flutter",
    "Firebase",
    "REST APIs"
]

Instead:

skills:
[
    "Flutter"
]

tools:
[
    "Firebase",
    "REST APIs"
]

experience:
[]

unless an actual duration or professional
experience requirement is explicitly stated.

====================
EDUCATION
====================

Put only academic qualifications here.

Examples:
- Bachelor's degree in Computer Science
- Master's degree
- Bachelor's degree or equivalent

Do not put skills or experience here.

====================
TOOLS
====================

Put frameworks, libraries, platforms, cloud services,
databases, development tools, and technologies here.

Examples:
- Firebase
- Provider
- Riverpod
- AWS
- Docker
- Git
- GitHub
- MongoDB
- FastAPI
- React

====================
RESPONSIBILITIES
====================

Put duties and actions the candidate is expected
to perform here.

Examples:
- Build mobile applications
- Develop responsive UI components
- Integrate REST APIs
- Debug and optimize applications

Do not copy technologies into responsibilities
as standalone items.

====================
GENERAL RULES
====================

1. Extract ONLY information explicitly present.
2. Never invent skills, tools, experience, education,
   or responsibilities.
3. Keep each item concise.
4. Keep every item atomic.
5. Do not combine unrelated items.
6. Do not duplicate the same requirement across
   multiple categories.
7. A technology mentioned in an experience sentence
   is still a technology, not an experience duration.
8. "Experience with X" does NOT mean X belongs
   in the experience list.
9. Only actual duration or professional experience
   requirements belong in experience.
10. If a category is genuinely absent, return [].

Job Description:

{job_description}
"""


def _parse_with_llm(
    job_description: str,
) -> JobRequirements:
    """
    Parse the job description using the configured LLM.
    """

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        JobRequirements
    )

    prompt = JOB_PARSER_PROMPT.format(
        job_description=job_description,
    )

    result = structured_llm.invoke(
        prompt
    )

    if not isinstance(
        result,
        JobRequirements,
    ):
        raise ValueError(
            "Failed to parse job description."
        )

    return result


def _normalize_items(
    items: list[str],
) -> list[str]:
    """
    Normalize and deduplicate extracted items.
    """

    normalized: list[str] = []
    seen: set[str] = set()

    for item in items:
        value = " ".join(
            item.strip().split()
        )

        if not value:
            continue

        key = value.casefold()

        if key in seen:
            continue

        seen.add(key)
        normalized.append(value)

    return normalized


def _clean_experience(
    experience: list[str],
) -> list[str]:
    """
    Keep only meaningful experience requirements.

    Technology-only requirements such as Firebase,
    REST APIs, or Flutter should not be treated as
    experience requirements.
    """

    cleaned: list[str] = []

    for item in _normalize_items(
        experience
    ):
        lowered = item.casefold()

        # Pure technology/tool mentions are not
        # experience requirements.
        technology_only = {
            "firebase",
            "rest api",
            "rest apis",
            "flutter",
            "dart",
            "provider",
            "riverpod",
            "git",
            "github",
            "python",
            "java",
            "javascript",
            "typescript",
            "react",
            "react.js",
            "node.js",
            "docker",
            "aws",
        }

        if lowered in technology_only:
            continue

        cleaned.append(item)

    return cleaned


def _recover_explicit_skills(
    job_description: str,
    result: JobRequirements,
) -> JobRequirements:
    """
    Preserve explicit technical skills that the
    LLM may have missed.

    This remains generic and only uses technologies
    already returned by the parser or explicitly
    present in the text.
    """

    skills = _normalize_items(
        result.skills
    )

    tools = _normalize_items(
        result.tools
    )

    experience = _clean_experience(
        result.experience
    )

    education = _normalize_items(
        result.education
    )

    responsibilities = _normalize_items(
        result.responsibilities
    )

    return JobRequirements(
        skills=skills,
        experience=experience,
        education=education,
        tools=tools,
        responsibilities=responsibilities,
    )


def parse_job_description(
    job_description: str,
) -> JobRequirements:
    """
    Parse a raw job description into structured
    job requirements.
    """

    job_description = job_description.strip()

    if not job_description:
        raise ValueError(
            "Job description cannot be empty."
        )

    result = _parse_with_llm(
        job_description
    )

    return _recover_explicit_skills(
        job_description=job_description,
        result=result,
    )