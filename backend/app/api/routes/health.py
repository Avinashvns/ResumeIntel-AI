from fastapi import APIRouter

from app.config.settings import get_settings

router = APIRouter(
    prefix= '/api/v1',
    tags=["Health"],
)


@router.get("/health")
def health_check():
    settings = get_settings()

    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }