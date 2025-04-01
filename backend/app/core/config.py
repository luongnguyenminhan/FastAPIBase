"""
Configuration Settings

This file defines the configuration settings for the application.
It loads environment variables and sets default values for various settings.

Dependencies:
- dotenv for environment variable management
- os for accessing environment variables

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

import os
from typing import Dict, Any
from pydantic import BaseSettings, validator
from dotenv import load_dotenv  # type: ignore

load_dotenv()


class AppSettings(BaseSettings):
    """Application settings class using Pydantic for type validation."""
    
    PROJECT_NAME: str = "FastAPI Project"
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"
    
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "******")
    DB_HOST: str = os.getenv("DB_HOST", "mysql")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "test")
    
    @property
    def DATABASE_URL(self) -> str:
        """Generate the database URL from individual components."""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Return the SQLAlchemy database URI."""
        return self.DATABASE_URL
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global instance for use throughout the application
settings = AppSettings()
