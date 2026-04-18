# Placeholder for FastAPI config using pydantic-settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Sentinel"
    # Add more settings as needed

settings = Settings()
