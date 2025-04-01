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

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


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


class ItemBusinessModel(BaseModel):
    """
    Core business model for Item entity

    Attributes:
        title (str): The title of the item
        description (Optional[str]): The description of the item
        price (Decimal): The price of the item
        category (Optional[str]): The category of the item
        is_active (bool): The active status of the item
        stock (int): The stock quantity of the item
    """
    title: str
    description: Optional[str] = None
    price: Decimal
    category: Optional[str] = None
    is_active: bool = True
    stock: int = 0