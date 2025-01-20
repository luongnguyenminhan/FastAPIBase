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
from dotenv import load_dotenv  # type: ignore

load_dotenv()

PROJECT_NAME = "FastAPI Project"
API_V1_STR = "/api/v1"
API_V2_STR = "/api/v2"
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "******")
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "test")
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SQLALCHEMY_DATABASE_URI = DATABASE_URL
