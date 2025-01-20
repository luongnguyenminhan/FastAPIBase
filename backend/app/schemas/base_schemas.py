"""
Base Schemas

This file defines the base schemas for user and item models.
These schemas are used as the foundation for other schemas in the application.

Dependencies:
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal

class UserBase(BaseModel):
    """
    Base schema for user model

    Attributes:
        email (str): The email of the user
        name (str): The name of the user
        is_active (Optional[bool]): The active status of the user, default is True
    """
    email: str
    name: str
    is_active: Optional[bool] = True

class ItemBase(BaseModel):
    """
    Base schema for item model

    Attributes:
        title (str): The title of the item
        description (Optional[str]): The description of the item
        price (Decimal): The price of the item
        category (Optional[str]): The category of the item
        is_active (bool): The active status of the item, default is True
        stock (int): The stock quantity of the item, default is 0
    """
    title: str
    description: Optional[str] = None
    price: Decimal
    category: Optional[str] = None
    is_active: bool = True
    stock: int = 0
