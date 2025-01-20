"""
Item Repository Implementation

This file defines the ItemRepository class for managing item-related database operations.
It inherits from BaseRepository and provides additional methods specific to items.

Dependencies:
- SQLAlchemy for database operations
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from .base_repository import BaseRepository
from app.db.models.items import Item
from sqlalchemy.orm import Session

class ItemRepository(BaseRepository[Item]):
    """
    Repository class for managing items

    Attributes:
        db (Session): The database session
    """

    def __init__(self, db: Session):
        """
        Initialize the item repository with a database session

        Args:
            db (Session): The database session
        """
        super().__init__(Item, db)

    def get_by_owner(self, owner_id: int):
        """
        Get items owned by a user

        Args:
            owner_id (int): The ID of the owner

        Returns:
            List[Item]: A list of items owned by the user
        """
        return self._dbSet.filter_by(owner_id=owner_id, is_deleted=False).all()
    
    def get_by_category(self, category: str):
        """
        Get items by category

        Args:
            category (str): The category of the items

        Returns:
            List[Item]: A list of items in the specified category
        """
        return self._dbSet.filter_by(category=category, is_deleted=False).all()
    
    def update_stock(self, id: int, quantity: int):
        """
        Update the stock of an item

        Args:
            id (int): The ID of the item
            quantity (int): The new quantity of the item

        Returns:
            int: The updated stock quantity of the item, or None if the item is not found
        """
        item = self.get_by_id(id)
        if item:
            item.stock = quantity
            self.update(item)
            return item.stock
        return None