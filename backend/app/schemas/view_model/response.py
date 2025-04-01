"""
Response View Models

This file defines the view models for outgoing response data.
These models handle response formatting and serialization.

Dependencies:
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from app.schemas.business_model.base import UserBusinessModel, ItemBusinessModel


class MessageResponseViewModel(BaseModel):
    """
    View model for generic message responses

    Attributes:
        message (str): The message content
    """
    message: str


class UserResponseViewModel(UserBusinessModel):
    """
    View model for user responses

    Extends UserBusinessModel with additional response-specific fields
    """
    id: int
    items_count: int = 0

    class Config:
        from_attributes = True


class ItemResponseViewModel(ItemBusinessModel):
    """
    View model for item responses

    Extends ItemBusinessModel with additional response-specific fields
    """
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class ItemWithOwnerViewModel(ItemResponseViewModel):
    """
    View model for item responses including owner details

    Attributes:
        owner (Optional[UserResponseViewModel]): The owner details
    """
    owner: Optional[UserResponseViewModel] = None


class UserMetricsResponseViewModel(BaseModel):
    """
    View model for user metrics responses

    Attributes:
        total (float): Sum of metrics
        average (float): Average of metrics
    """
    total: float
    average: float


class ItemValueResponseViewModel(BaseModel):
    """
    View model for item value calculation responses

    Attributes:
        item_id (int): Item identifier
        quantity (int): Quantity of items
        total_value (Decimal): Total calculated value
    """
    item_id: int
    quantity: int
    total_value: Decimal


class ItemDiscountResponseViewModel(BaseModel):
    """
    View model for item discount calculation responses

    Attributes:
        item_id (int): Item identifier
        original_price (Decimal): Original price before discount
        discount_percentage (float): Applied discount percentage
        final_price (Decimal): Final price after discount
    """
    item_id: int
    original_price: Decimal
    discount_percentage: float
    final_price: Decimal