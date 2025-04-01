"""
Request View Models

This file defines the view models for incoming request data.
These models handle request validation and data transformation.

Dependencies:
- Pydantic for data validation and serialization
- Email validator for email validation

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from decimal import Decimal
from app.schemas.business_model.base import UserBusinessModel, ItemBusinessModel


class UserRequestViewModel(UserBusinessModel):
    """
    View model for user creation/update requests

    Extends UserBusinessModel with additional request-specific fields
    """
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "secretpassword",
                "is_active": True
            }
        }


class ItemRequestViewModel(ItemBusinessModel):
    """
    View model for item creation/update requests

    Extends ItemBusinessModel with additional request-specific fields
    """
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


class ItemStockUpdateViewModel(BaseModel):
    """
    View model for item stock updates

    Attributes:
        quantity (int): The new quantity of the item
    """
    quantity: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "quantity": 10
            }
        }


class MathOperationViewModel(BaseModel):
    """
    View model for mathematical operations

    Attributes:
        x (float): First operand
        y (float): Second operand
    """
    x: float = Field(..., description="First number")
    y: float = Field(..., description="Second number")


class UserMetricsViewModel(BaseModel):
    """
    View model for user metrics calculation

    Attributes:
        metric_values (List[float]): Values to calculate metrics for
    """
    metric_values: List[float] = Field(..., description="List of metric values to calculate")