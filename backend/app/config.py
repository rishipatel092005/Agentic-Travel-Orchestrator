"""
Configuration management using Pydantic Settings.
Loads environment variables from .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional


project_root = Path(__file__).resolve().parents[2]
env_file = project_root / ".env"
if not env_file.exists():
    env_file = project_root / "backend" / ".env"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All API keys are optional to support local development.
    Do not expose these in logs or responses.
    """
    
    # Database
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "agentic_travel_planner"
    
    # API Keys (optional)
    groq_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    openweathermap_api_key: Optional[str] = None
    gplaces_api_key: Optional[str] = None
    exchange_rate_api_key: Optional[str] = None
    
    # Application settings
    debug: bool = False
    app_name: str = "Agentic Travel Planner"
    
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()
