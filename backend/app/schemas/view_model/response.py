"""
Response View Models

This file defines the view models for outgoing response data.
These models handle response formatting and serialization.

Dependencies:
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.0.1
"""

from decimal import Decimal
from typing import List, Optional, Dict, Any, Set

from app.schemas.business_model.base import UserBusinessModel, ItemBusinessModel
from pydantic import BaseModel


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


class OperationResultViewModel(BaseModel):
    """
    View model for standard operation results

    Attributes:
        success (bool): Indicates if the operation was successful
        message (str): A descriptive message about the operation
        data (Optional[Dict[str, Any]]): Optional data returned from the operation
    """
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class EnhancedOperationResultViewModel(OperationResultViewModel):
    """
    Extended view model for operation results with additional metadata

    Attributes:
        success (bool): Indicates if the operation was successful
        message (str): A descriptive message about the operation
        data (Optional[Dict[str, Any]]): Optional data returned from the operation
        metadata (Dict[str, Any]): Additional metadata about the operation
        operation_id (Optional[str]): Unique identifier for the operation
    """
    metadata: Dict[str, Any] = {}
    operation_id: Optional[str] = None


class EnhancedUserResponseViewModel(UserResponseViewModel):
    """
    Enhanced view model for detailed user responses
    
    Extends UserResponseViewModel with additional user details and metadata
    
    Attributes:
        items (List[ItemResponseViewModel]): List of items owned by the user
        roles (Set[str]): User roles/permissions
        is_active (bool): User account status
        last_login (Optional[str]): Timestamp of last login
        metadata (Dict[str, Any]): Additional user metadata
    """
    items: List[ItemResponseViewModel] = []
    roles: Set[str] = set()
    is_active: bool = True
    last_login: Optional[str] = None
    metadata: Dict[str, Any] = {}

    class Config:
        from_attributes = True
