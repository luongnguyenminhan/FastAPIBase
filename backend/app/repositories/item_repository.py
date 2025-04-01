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
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


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
        logger.info("ItemRepository initialized")

    def get_by_owner(self, owner_id: int) -> List[Item]:
        """
        Get items owned by a user

        Args:
            owner_id (int): The ID of the owner

        Returns:
            List[Item]: A list of items owned by the user
        """
        logger.debug(f"Getting items for owner_id: {owner_id}")
        return self._dbSet.filter_by(owner_id=owner_id, is_deleted=False).all()

    def get_by_category(self, category: str) -> List[Item]:
        """
        Get items by category

        Args:
            category (str): The category of the items

        Returns:
            List[Item]: A list of items in the specified category
        """
        logger.debug(f"Getting items for category: {category}")
        return self._dbSet.filter_by(category=category, is_deleted=False).all()

    def update_stock(self, id: int, quantity: int) -> Optional[int]:
        """
        Update the stock of an item

        Args:
            id (int): The ID of the item
            quantity (int): The new quantity of the item

        Returns:
            Optional[int]: The updated stock quantity of the item, or None if the item is not found
        """
        try:
            item: Optional[Item] = self.get_by_id(id)
            if item:
                item.stock = quantity
                self.update(item)
                logger.info(f"Updated stock for item id {id} to {quantity}")
                return item.stock
            logger.warning(f"Attempted to update stock for non-existent item id: {id}")
            return None
        except Exception as e:
            logger.error(f"Error updating stock for item id {id}: {str(e)}")
            raise
