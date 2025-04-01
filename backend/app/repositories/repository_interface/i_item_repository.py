"""
Item Repository Interface

This file defines the ItemRepositoryInterface for managing item-related database operations.
It inherits from IRepository and defines the interface for item repository implementations.

Dependencies:
- SQLAlchemy for database operations
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 2024
Version: 1.0.0
"""

from abc import abstractmethod
from typing import List, Optional

from app.db.models.items import Item

from .i_base_repository import IRepository


class IItemRepository(IRepository[Item]):
    """Repository interface for managing items"""

    @abstractmethod
    def get_by_owner(self, owner_id: int) -> List[Item]:
        """Get items owned by a user"""
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Item]:
        """Get items by category"""
        pass

    @abstractmethod
    def update_stock(self, id: int, quantity: int) -> Optional[int]:
        """Update the stock of an item"""
        pass
