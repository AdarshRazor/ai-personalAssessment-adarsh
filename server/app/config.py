import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Personality Assessment System"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./personality_assessment.db")
    
    # OpenRouter settings
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_URL: str = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1")
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000"]  # Frontend URL

    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")

settings = Settings()