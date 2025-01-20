"""
Response Schemas

This file defines the schemas for various response payloads used in the application.
These schemas are used to validate and serialize outgoing response data.

Dependencies:
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal


# Generic responses
class MessageResponse(BaseModel):
    """
    Schema for generic message response

    Attributes:
        message (str): The message content
    """
    message: str


class EchoResponse(BaseModel):
    """
    Schema for echo response

    Attributes:
        echo (str): The echoed message
        version (str): The version of the API
    """
    echo: str
    version: str


# User related responses
class UserResponse(BaseModel):
    """
    Schema for user response

    Attributes:
        id (int): The ID of the user
        email (str): The email of the user
        name (str): The name of the user
        is_active (bool): The active status of the user
        items_count (int): The count of items owned by the user, default is 0
    """
    id: int
    email: str
    name: str
    is_active: bool
    items_count: int = 0

    class Config:
        from_attributes = True


class UserMetricsResponse(BaseModel):
    """
    Schema for user metrics response

    Attributes:
        total (float): The total of the metric values
        average (float): The average of the metric values
    """
    total: float
    average: float


# Item related responses
class ItemResponse(BaseModel):
    """
    Schema for item response

    Attributes:
        id (int): The ID of the item
        title (str): The title of the item
        description (Optional[str]): The description of the item
        price (Decimal): The price of the item
        category (Optional[str]): The category of the item
        is_active (bool): The active status of the item
        stock (int): The stock quantity of the item
        owner_id (int): The ID of the owner
    """
    id: int
    title: str
    description: Optional[str]
    price: Decimal
    category: Optional[str]
    is_active: bool
    stock: int
    owner_id: int

    class Config:
        from_attributes = True


class ItemWithOwnerResponse(ItemResponse):
    """
    Schema for item response with owner details

    Attributes:
        owner (Optional[UserResponse]): The owner details of the item
    """
    owner: Optional[UserResponse] = None


class ItemValueResponse(BaseModel):
    """
    Schema for item value response

    Attributes:
        item_id (int): The ID of the item
        quantity (int): The quantity of the item
        total_value (Decimal): The total value of the item
    """
    item_id: int
    quantity: int
    total_value: Decimal


class ItemDiscountResponse(BaseModel):
    """
    Schema for item discount response

    Attributes:
        item_id (int): The ID of the item
        original_price (Decimal): The original price of the item
        discount_percentage (float): The discount percentage
        final_price (Decimal): The final price of the item after discount
    """
    item_id: int
    original_price: Decimal
    discount_percentage: float
    final_price: Decimal
