import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from colorama import Fore, Back
from typing import List
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

class Settings(BaseSettings):
    APP_NAME:    str
    APP_VERSION: str

    LLM_PROVIDER: str

    IMAGE_MAX_SIZE:       int
    IMAGES_ALLOWED_TYPES: List[str]

    FILE_MAX_SIZE:        int
    FILE_ALLOWED_TYPES:   List[str]

    MISTRAL_MODEL:   str
    MISTRAL_API_KEY: str
    
    GROQ_MODEL: str
    GROQ_API_KEY: str

    OLLAMA_MODEL:    str

    model_config = SettingsConfigDict(
    env_file=ENV_PATH if ENV_PATH.exists() else None,    # For Streamlit Cloud Deployment
    env_file_encoding="utf-8"
    )


def get_settings():
    return Settings() # type: ignore


if __name__ == "__main__":
    print(  Fore.RED + f'Mistral API_KEY: { get_settings().MISTRAL_API_KEY } ' + Fore.RESET )
    