from fastapi import (
    APIRouter,
    HTTPException,
)

from app.job.experience import (
    match_experience,
)
from app.job.matching import (
    find_missing_skills,
    match_skills,
    merge_job_skills,
)
from app.job.parser import (
    parse_job_description,
)
from app.job.recommendations import (
    generate_recommendations,
)
from app.job.resume_profile import (
    extract_resume_profile,
)
from app.job.scoring import (
    calculate_match_score,
)
from app.job.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ResumeProfileResponse,
)


router = APIRouter(
    prefix="/analyze",
    tags=["Job Analysis"],
)


@router.post(
    "",
    response_model=AnalyzeResponse,
)
def analyze_resume(
    request: AnalyzeRequest,
) -> AnalyzeResponse:
    """
    Analyze an uploaded resume against
    a provided job description.
    """

    stored_filename = (
        request.stored_filename.strip()
    )

    job_description = (
        request.job_description.strip()
    )

    if not stored_filename:
        raise HTTPException(
            status_code=400,
            detail="stored_filename cannot be empty.",
        )

    if not job_description:
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    try:
        resume_profile = (
            extract_resume_profile(
                stored_filename
            )
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    try:
        job_requirements = (
            parse_job_description(
                job_description
            )
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    # Combine job skills and tools into one
    # generic matching pool.
    matchable_job_skills = (
        merge_job_skills(
            skills=job_requirements.skills,
            tools=job_requirements.tools,
        )
    )

    skill_match = match_skills(
        resume_skills=resume_profile.skills,
        job_skills=matchable_job_skills,
    )

    missing_skill_result = (
        find_missing_skills(
            resume_skills=resume_profile.skills,
            job_skills=matchable_job_skills,
        )
    )

    experience_match = match_experience(
        resume_experience=(
            resume_profile.experience
        ),
        job_experience=(
            job_requirements.experience
        ),
    )

    score = calculate_match_score(
        total_job_skills=len(
            matchable_job_skills
        ),
        matched_skills=len(
            skill_match.matched_skills
        ),
        total_job_experience=len(
            job_requirements.experience
        ),
        matched_experience=len(
            experience_match.matched_experience
        ),
    )

    recommendation_result = (
        generate_recommendations(
            matched_skills=(
                skill_match.matched_skills
            ),
            missing_skills=(
                missing_skill_result.missing_skills
            ),
            matched_experience=(
                experience_match.matched_experience
            ),
            unmatched_experience=(
                experience_match.unmatched_experience
            ),
        )
    )

    return AnalyzeResponse(
        stored_filename=stored_filename,
        resume_profile=ResumeProfileResponse(
            skills=resume_profile.skills,
            experience=resume_profile.experience,
        ),
        job_requirements=job_requirements,
        matched_skills=(
            skill_match.matched_skills
        ),
        missing_skills=(
            missing_skill_result.missing_skills
        ),
        matched_experience=(
            experience_match.matched_experience
        ),
        unmatched_experience=(
            experience_match.unmatched_experience
        ),
        skill_score=score.skill_score,
        experience_score=(
            score.experience_score
        ),
        overall_score=score.overall_score,
        recommendations=(
            recommendation_result.recommendations
        ),
    )