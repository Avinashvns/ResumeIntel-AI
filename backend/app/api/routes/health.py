from fastapi import APIRouter

from app.config.settings import get_settings
from app.schemas.common import HealthResponse

router = APIRouter(
    prefix= '/api/v1',
    tags=["Health"],
)


@router.get("/health" , response_model=HealthResponse)
def health_check() -> HealthResponse:
    settings = get_settings()

    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )