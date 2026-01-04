from pydantic_settings import BaseSettings
from typing import Optional, List
import secrets


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://learnify:learnify@postgres:5432/learnify"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600
    
    # API
    API_V1_PREFIX: str = "/api"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://frontend:80", "http://localhost:5173"]
    
    # JWT Settings
    SECRET_KEY: str = "super-secret-key-for-dev" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15 
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30 
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

