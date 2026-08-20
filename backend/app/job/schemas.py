from pydantic import BaseModel, Field


class JobRequirements(BaseModel):
    """
    Structured requirements extracted from a
    job description.
    """

    skills: list[str] = Field(
        default_factory=list,
        description="Required technical and domain skills.",
    )

    experience: list[str] = Field(
        default_factory=list,
        description="Required or preferred experience.",
    )

    education: list[str] = Field(
        default_factory=list,
        description="Required or preferred education.",
    )

    tools: list[str] = Field(
        default_factory=list,
        description="Tools, frameworks, platforms, and technologies.",
    )

    responsibilities: list[str] = Field(
        default_factory=list,
        description="Responsibilities mentioned in the job description.",
    )