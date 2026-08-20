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


class AnalyzeRequest(BaseModel):
    """
    Request payload for resume-job analysis.
    """

    stored_filename: str = Field(
        min_length=1,
        description="Stored resume filename returned by upload.",
    )

    job_description: str = Field(
        min_length=1,
        description="Job description to analyze against the resume.",
    )


class ResumeProfileResponse(BaseModel):
    """
    Structured resume information.
    """

    skills: list[str] = Field(
        default_factory=list,
    )

    experience: list[str] = Field(
        default_factory=list,
    )


class AnalyzeResponse(BaseModel):
    """
    Complete resume-to-job analysis result.
    """

    stored_filename: str

    resume_profile: ResumeProfileResponse

    job_requirements: JobRequirements

    matched_skills: list[str] = Field(
        default_factory=list,
    )

    missing_skills: list[str] = Field(
        default_factory=list,
    )

    matched_experience: list[str] = Field(
        default_factory=list,
    )

    unmatched_experience: list[str] = Field(
        default_factory=list,
    )

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

    recommendations: list[str] = Field(
        default_factory=list,
    )