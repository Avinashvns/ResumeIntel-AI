from fastapi import FastAPI

from app.config.settings import get_settings
from app.api.routes.health import router as health_router


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="MCP-Enabled Agentic RAG Resume Intelligence System",
)

app.include_router(health_router)