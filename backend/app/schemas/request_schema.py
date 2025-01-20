"""
Request Schemas

This file defines the schemas for various request payloads used in the application.
These schemas are used to validate and serialize incoming request data.

Dependencies:
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from decimal import Decimal


# Math Operation Request
class MathOperationRequest(BaseModel):
    """
    Schema for math operation request

    Attributes:
        x (float): The first number
        y (float): The second number
    """
    x: float = Field(..., description="First number")
    y: float = Field(..., description="Second number")


# User related requests
class UserRequest(BaseModel):
    """
    Schema for user creation request

    Attributes:
        email (EmailStr): The email of the user
        name (str): The name of the user
        password (str): The password of the user
        is_active (Optional[bool]): The active status of the user, default is True
    """
    email: EmailStr
    name: str
    password: str
    is_active: Optional[bool] = True

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "secretpassword",
                "is_active": True
            }
        }


class UserMetricsRequest(BaseModel):
    """
    Schema for user metrics request

    Attributes:
        metric_values (List[float]): List of metric values to calculate
    """
    metric_values: List[float] = Field(..., description="List of metric values to calculate")


# Item related requests
class ItemRequest(BaseModel):
    """
    Schema for item creation request

    Attributes:
        title (str): The title of the item
        description (Optional[str]): The description of the item
        price (Decimal): The price of the item
        category (Optional[str]): The category of the item
        is_active (bool): The active status of the item, default is True
        stock (int): The stock quantity of the item, default is 0
        owner_id (Optional[int]): The ID of the owner
    """
    title: str
    description: Optional[str] = None
    price: Decimal
    category: Optional[str] = None
    is_active: bool = True
    stock: int = 0
    owner_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Sample Item",
                "description": "A sample item description",
                "price": "29.99",
                "category": "electronics",
                "stock": 100,
                "owner_id": 1
            }
        }


class ItemUpdateRequest(BaseModel):
    """
    Schema for item update request

    Attributes:
        title (Optional[str]): The title of the item
        description (Optional[str]): The description of the item
        price (Optional[Decimal]): The price of the item
        category (Optional[str]): The category of the item
        is_active (Optional[bool]): The active status of the item
        stock (Optional[int]): The stock quantity of the item
    """
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None
    stock: Optional[int] = None


class ItemStockUpdateRequest(BaseModel):
    """
    Schema for item stock update request

    Attributes:
        quantity (int): The new quantity of the item, must be greater than 0
    """
    quantity: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "quantity": 10
            }
        }


class ItemDiscountRequest(BaseModel):
    """
    Schema for item discount request

    Attributes:
        price (float): The original price of the item, must be greater than 0
        discount_percentage (float): The discount percentage, must be between 0 and 100
    """
    price: float = Field(..., gt=0, description="Original price")
    discount_percentage: float = Field(..., ge=0, le=100, description="Discount percentage")
