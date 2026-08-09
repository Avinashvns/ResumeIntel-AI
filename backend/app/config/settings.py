from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ResumeIntel AI"
    app_version: str = "0.1.0"
    environment: str = "development"

    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "qwen3:4b"

    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    faiss_index_path: str = "../data/vector_store"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()