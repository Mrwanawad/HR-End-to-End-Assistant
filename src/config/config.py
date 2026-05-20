import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from colorama import Fore
from typing import List
from pathlib import Path
import json

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

    OLLAMA_MODEL: str

    @field_validator("IMAGES_ALLOWED_TYPES", "FILE_ALLOWED_TYPES", mode="before")
    @classmethod
    def parse_list(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

    model_config = SettingsConfigDict(
        env_file=ENV_PATH if ENV_PATH.exists() else None,
        env_file_encoding="utf-8"
    )


def get_settings():
    return Settings() # type: ignore