from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from colorama import Fore

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

class Settings(BaseSettings):
    APP_NAME:    str
    APP_VERSION: str

    LLM_PROVIDER: str

    IMAGE_MAX_SIZE:       int = 10
    IMAGES_ALLOWED_TYPES: List[str] = ["image/png", "image/jpg", "image/jpeg"]

    FILE_MAX_SIZE:        int = 100
    FILE_ALLOWED_TYPES:   List[str] = ["text/plain", "application/pdf", "application/docx"]

    MISTRAL_MODEL:   str
    MISTRAL_API_KEY: str

    GROQ_MODEL:   str
    GROQ_API_KEY: str

    OLLAMA_MODEL: str

    model_config = SettingsConfigDict(
        env_file=ENV_PATH if ENV_PATH.exists() else None,
        env_file_encoding="utf-8"
    )


def get_settings():
    return Settings() # type: ignore