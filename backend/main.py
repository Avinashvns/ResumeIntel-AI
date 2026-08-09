from fastapi import FastAPI

from app.config.settings import get_settings
from app.api.routes.health import router as health_router
from app.exceptions.handlers import generic_exception_handler
from fastapi.middleware.cors import CORSMiddleware


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="MCP-Enabled Agentic RAG Resume Intelligence System",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)


app.include_router(health_router)