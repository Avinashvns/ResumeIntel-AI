from app.job.schemas import (
    JobRequirements,
)
from app.llm.ollama_client import (
    get_llm,
)


JOB_PARSER_PROMPT = """
You are a strict Job Description Information Extraction system.

Extract ONLY information explicitly present in the
provided Job Description.

Return these five categories:

skills:
Programming languages, AI/ML skills, domain skills,
and technical competencies.

experience:
Years of experience and professional experience requirements.

education:
Degrees, certifications, and academic qualifications.

tools:
Frameworks, libraries, platforms, cloud services,
databases, and software tools.

responsibilities:
Duties and actions the candidate is expected to perform.

Rules:
- Extract every explicitly mentioned relevant item.
- Never invent information.
- Do not put tools inside experience.
- Do not put education inside experience.
- Do not put responsibilities inside skills.
- If information exists for a category, do not return
  an empty list.
- Keep each extracted item concise.
- Return an empty list only when the category is genuinely
  absent from the job description.

Job Description:

{job_description}
"""


SKILL_TERMS = (
    "Python",
    "PyTorch",
    "TensorFlow",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "RAG",
    "Generative AI",
    "SQL",
)


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


def _recover_skills(
    job_description: str,
    result: JobRequirements,
) -> JobRequirements:
    """
    Recover known skills that are explicitly present
    in the job description but were missed by the LLM.
    """

    existing = {
        skill.strip().lower()
        for skill in result.skills
    }

    skills = list(result.skills)

    job_text = job_description.lower()

    for skill in SKILL_TERMS:

        if (
            skill.lower() in job_text
            and skill.lower() not in existing
        ):
            skills.append(skill)

    return JobRequirements(
        skills=skills,
        experience=result.experience,
        education=result.education,
        tools=result.tools,
        responsibilities=result.responsibilities,
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

    result = _recover_skills(
        job_description,
        result,
    )

    return result