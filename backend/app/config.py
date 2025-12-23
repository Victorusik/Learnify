from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://learnify:learnify@postgres:5432/learnify"
    
    # API
    API_V1_PREFIX: str = "/api"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://frontend:80"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

