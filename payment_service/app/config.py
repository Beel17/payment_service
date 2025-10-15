"""
Configuration settings for FastAPI Payment Service
Set environment variables in Render dashboard for production
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file (development only)
load_dotenv()

class Settings:
    # Paystack Configuration
    PAYSTACK_SECRET_KEY: str = os.getenv("PAYSTACK_SECRET_KEY", "")
    PAYSTACK_PUBLIC_KEY: str = os.getenv("PAYSTACK_PUBLIC_KEY", "")
    PAYSTACK_BASE_URL: str = "https://api.paystack.co"
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./payment_service.db")
    
    # App Configuration
    APP_NAME: str = "FastAPI Payment Service"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # CORS - Support both local and production origins
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS", 
        "http://localhost:3000,http://localhost:8000"
    ).split(",")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Render specific settings
    RENDER: bool = os.getenv("RENDER", "false").lower() == "true"

settings = Settings()
