# Configuration settings for the AI Personality Assessment System
# This file manages environment variables and application settings

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Basic application information
    PROJECT_NAME: str = "AI Personality Assessment System"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database configuration
    # Uses SQLite by default, but can be configured for other databases via environment variable
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./personality_assessment.db")
    
    # OpenRouter AI service configuration
    # Required for generating questions and analyzing responses
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_URL: str = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1")
    
    # CORS configuration for frontend communication
    # Add additional origins as needed for different environments
    CORS_ORIGINS: list = ["http://localhost:3000"]  # Frontend URL

    # JWT authentication configuration
    # IMPORTANT: Change the secret key in production!
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")

# Create a singleton instance of Settings
settings = Settings()