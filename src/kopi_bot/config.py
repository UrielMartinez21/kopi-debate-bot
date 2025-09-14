"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    app_name: str = "Kopi Debate Bot"
    debug: bool = False
    log_level: str = "INFO"
    
    # Database Configuration
    database_url: str = "sqlite:///./kopi_debate.db"
    
    # OpenAI Configuration (for AI-powered responses)
    openai_api_key: Optional[str] = None
    
    # Conversation Settings
    max_conversation_history: int = 5
    max_message_length: int = 2000
    response_timeout: int = 30
    
    class Config:
        """Pydantic settings config"""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()