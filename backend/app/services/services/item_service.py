"""
Item Service Implementation

This file defines the ItemService class, which provides methods for managing items.
It inherits from BaseService and uses the Unit of Work pattern for transaction management.

Dependencies:
- FastAPI for dependency injection and HTTP exceptions
- SQLAlchemy for database operations
- Unit of Work pattern for transaction management
- Repository pattern for data access
- MathOperations utility class for performing calculations

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.0.0
"""

import logging
from typing import List, Optional

from app.db.base import get_db
from app.db.models import User
from app.db.models.items import Item
from app.repositories.item_repository import ItemRepository
from app.services.service_interface.i_item_service import IItemService
from app.services.utils.example_core import MathOperations
from app.services.utils.exceptions.exceptions import (
    NotFoundException,
    BadRequestException,
    InternalServerException
)
from app.unit_of_work.unit_of_work import UnitOfWork
from fastapi import Depends
from sqlalchemy.orm import Session

from .base_service import BaseService, service_method

logger = logging.getLogger(__name__)


class ItemService(BaseService[Item], IItemService):
    """
    Service class for managing items

    Attributes:
        uow (UnitOfWork): The Unit of Work instance for managing transactions
    """

    def __init__(self, uow: UnitOfWork):
        """
        Initialize the item service with a Unit of Work

        Args:
            uow (UnitOfWork): The Unit of Work instance for managing transactions
        """
        super().__init__(uow)
        logger.info("ItemService initialized")

    @service_method
    async def get_by_owner(self, owner_id: int) -> List[Item]:
        """
        Get items owned by a user

        Args:
            owner_id (int): The ID of the owner

        Returns:
            List[Item]: A list of items owned by the user

        Raises:
            NotFoundException: If the owner is not found
        """
        logger.debug(f"Getting items for owner ID: {owner_id}")
        user: Optional[User] = self.uow.user_repository.get_by_id(owner_id)
        if not user:
            logger.warning(f"Owner with ID {owner_id} not found")
            raise NotFoundException(
                error_code="OWNER_NOT_FOUND",
                message=f"Owner with id {owner_id} not found"
            )
        return self.uow.item_repository.get_by_owner(owner_id)

    @service_method
    async def get_by_category(self, category: str) -> List[Item]:
        """
        Get items by category

        Args:
            category (str): The category of the items

        Returns:
            List[Item]: A list of items in the specified category
        """
        logger.debug(f"Getting items for category: {category}")
        return self.uow.item_repository.get_by_category(category)

    @service_method
    async def update_stock(self, id: int, quantity: int) -> Optional[int]:
        """
        Update the stock of an item

        Args:
            id (int): The ID of the item
            quantity (int): The new quantity of the item

        Returns:
            Optional[int]: The updated stock quantity or None if item not found
        """
        try:
            logger.info(f"Updating stock for item ID {id} to {quantity}")
            with self.uow:
                updated_stock: Optional[int] = self.uow.item_repository.update_stock(id, quantity)
                if updated_stock is None:
                    logger.warning(f"Item with ID {id} not found for stock update")
                    raise NotFoundException(
                        error_code="ITEM_NOT_FOUND",
                        message=f"Item with id {id} not found"
                    )
                self.uow.commit()
                logger.info(f"Updated stock for item ID {id} to {quantity}")
                return updated_stock
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error updating stock for item ID {id}: {str(e)}")
            self.uow.rollback()
            raise InternalServerException(
                error_code="STOCK_UPDATE_ERROR",
                message=f"Failed to update stock: {str(e)}"
            )

    @service_method
    async def calculate_total_value(self, price: float, quantity: int) -> float:
        """
        Calculate the total value of items

        Args:
            price (float): The price of a single item
            quantity (int): The quantity of items

        Returns:
            float: The total value of the items
        """
        logger.debug(f"Calculating total value for price: {price}, quantity: {quantity}")
        total_value: float = MathOperations.multiply(price, quantity)
        return total_value

    @service_method
    async def calculate_discount(self, price: float, discount_percentage: float) -> float:
        """
        Calculate the discounted price of an item

        Args:
            price (float): The original price of the item
            discount_percentage (float): The discount percentage

        Returns:
            float: The discounted price of the item
            
        Raises:
            BadRequestException: If the discount percentage is invalid
        """
        logger.debug(f"Calculating discount for price: {price}, discount: {discount_percentage}%")
        if discount_percentage < 0 or discount_percentage > 100:
            raise BadRequestException(
                error_code="INVALID_DISCOUNT_PERCENTAGE",
                message="Discount percentage must be between 0 and 100"
            )

        try:
            discount_rate: float = MathOperations.divide(discount_percentage, 100)
            discount_amount: float = MathOperations.multiply(price, discount_rate)
            discounted_price: float = MathOperations.subtract(price, discount_amount)
            return discounted_price
        except ValueError as e:
            raise BadRequestException(
                error_code="CALCULATION_ERROR",
                message=str(e)
            )

    @service_method
    async def get(self, id: int) -> Item:
        """
        Get an item by ID

        Args:
            id (int): The ID of the item

        Returns:
            Item: The item with the specified ID

        Raises:
            NotFoundException: If the item is not found
        """
        logger.debug(f"Getting item by ID: {id}")
        item: Optional[Item] = self.uow.item_repository.get_by_id(id)
        if not item:
            logger.warning(f"Item with ID {id} not found")
            raise NotFoundException(
                error_code="ITEM_NOT_FOUND",
                message=f"Item with id {id} not found"
            )
        return item

    @service_method
    async def create(self, item: Item) -> Item:
        """
        Create a new item

        Args:
            item (Item): The item to create

        Returns:
            Item: The created item
        """
        try:
            logger.info(f"Creating new item with title: {item.title}")
            with self.uow:
                created_item: Item = self.uow.item_repository.add(item)
                self.uow.commit()
            logger.info(f"Created item with ID: {created_item.id}")
            return created_item
        except Exception as e:
            logger.error(f"Error creating item: {str(e)}")
            self.uow.rollback()
            raise InternalServerException(
                error_code="ITEM_CREATION_ERROR",
                message=f"Failed to create item: {str(e)}"
            )

    @service_method
    async def update(self, item: Item) -> Item:
        """
        Update an existing item

        Args:
            item (Item): The item to update

        Returns:
            Item: The updated item
        """
        try:
            logger.info(f"Updating item with ID: {item.id}")
            with self.uow:
                existing_item: Optional[Item] = self.uow.item_repository.get_by_id(item.id)
                if not existing_item:
                    logger.warning(f"Item with ID {item.id} not found for update")
                    raise NotFoundException(
                        error_code="ITEM_NOT_FOUND",
                        message=f"Item with id {item.id} not found"
                    )

                self.uow.item_repository.update(item)
                self.uow.commit()
            logger.info(f"Updated item with ID: {item.id}")
            return item
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error updating item: {str(e)}")
            self.uow.rollback()
            raise InternalServerException(
                error_code="ITEM_UPDATE_ERROR",
                message=f"Failed to update item: {str(e)}"
            )

    @service_method
    async def delete(self, id: int) -> None:
        """
        Delete an item by ID

        Args:
            id (int): The ID of the item to delete

        Returns:
            None

        Raises:
            NotFoundException: If the item is not found
        """
        try:
            logger.info(f"Deleting item with ID: {id}")
            with self.uow:
                item: Optional[Item] = self.uow.item_repository.get_by_id(id)
                if not item:
                    logger.warning(f"Item with ID {id} not found for deletion")
                    raise NotFoundException(
                        error_code="ITEM_NOT_FOUND",
                        message=f"Item with id {id} not found"
                    )

                self.uow.item_repository.soft_delete(item)
                self.uow.commit()
            logger.info(f"Deleted item with ID: {id}")
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error deleting item: {str(e)}")
            self.uow.rollback()
            raise InternalServerException(
                error_code="ITEM_DELETION_ERROR",
                message=f"Failed to delete item: {str(e)}"
            )

    @staticmethod
    def get_self(db: Session = Depends(get_db)) -> 'ItemService':
        """
        Get the item service instance

        Args:
            db (Session): The database session, injected by FastAPI

        Returns:
            ItemService: The item service instance
        """
        uow = UnitOfWork(db)
        return ItemService(uow)
