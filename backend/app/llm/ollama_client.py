from langchain_ollama import ChatOllama

from app.config.settings import get_settings


def get_llm() -> ChatOllama:
    """
    Create the local LLM client used by ResumeIntel AI.
    """
    settings = get_settings()

    return ChatOllama(
        model= settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )