"""
Base Business Models

This file defines the core business models used across the application.
These models represent the fundamental business entities and their attributes.

Dependencies:
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class UserBusinessModel(BaseModel):
    """
    Core business model for User entity

    Attributes:
        email (str): The email of the user
        name (str): The name of the user
        is_active (Optional[bool]): The active status of the user
    """
    email: str
    name: str
    is_active: Optional[bool] = True
