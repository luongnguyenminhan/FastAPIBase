"""
Item Service Interface Definition

This file defines the service interface for managing item-related business logic.
It inherits from IBaseService and defines the interface for item service implementations.

Dependencies:
- FastAPI for dependency injection
- SQLAlchemy for database operations

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.0.0
"""

from abc import abstractmethod
from typing import List, Optional

from app.db.models.items import Item
from app.services.service_interface.i_base_service import IBaseService


class IItemService(IBaseService[Item]):
    """Interface for item service operations"""

    @abstractmethod
    async def get_by_owner(self, owner_id: int) -> List[Item]:
        """Get items owned by a user"""
        pass

    @abstractmethod
    async def get_by_category(self, category: str) -> List[Item]:
        """Get items by category"""
        pass

    @abstractmethod
    async def update_stock(self, id: int, quantity: int) -> Optional[int]:
        """Update the stock of an item"""
        pass

    @abstractmethod
    async def calculate_total_value(self, price: float, quantity: int) -> float:
        """Calculate the total value of items"""
        pass

    @abstractmethod
    async def calculate_discount(self, price: float, discount_percentage: float) -> float:
        """Calculate the discounted price of an item"""
        pass

    @abstractmethod
    async def get(self, id: int) -> Item:
        """Get an item by ID"""
        pass

    @abstractmethod
    async def create(self, item: Item) -> Item:
        """Create a new item"""
        pass

    @abstractmethod
    async def update(self, item: Item) -> Item:
        """Update an existing item"""
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        """Delete an item by ID"""
        pass
