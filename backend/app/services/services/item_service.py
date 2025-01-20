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
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from fastapi import HTTPException, status, Depends
from .base_service import BaseService, service_method
from app.db.models import Item
from app.repositories.item_repository import ItemRepository
from app.services.utils.example_core import MathOperations
from app.unit_of_work.unit_of_work import UnitOfWork
from sqlalchemy.orm import Session
from app.db.base import get_db

class ItemService(BaseService[Item]):
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

    @service_method
    async def get_by_owner(self, owner_id: int):
        """
        Get items owned by a user

        Args:
            owner_id (int): The ID of the owner

        Returns:
            List[Item]: A list of items owned by the user

        Raises:
            HTTPException: If the owner is not found
        """
        user = self.uow.user_repository.get_by_id(owner_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Owner with id {owner_id} not found"
            )
        return self.uow.item_repository.get_by_owner(owner_id)

    @service_method
    async def get_by_category(self, category: str):
        """
        Get items by category

        Args:
            category (str): The category of the items

        Returns:
            List[Item]: A list of items in the specified category
        """
        return self.uow.item_repository.get_by_category(category)

    @service_method
    async def update_stock(self, id: int, quantity: int):
        """
        Update the stock of an item

        Args:
            id (int): The ID of the item
            quantity (int): The new quantity of the item

        Returns:
            Item: The updated item
        """
        return self.uow.item_repository.update_stock(id, quantity)

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
        return MathOperations.multiply(price, quantity)

    @service_method
    async def calculate_discount(self, price: float, discount_percentage: float) -> float:
        """
        Calculate the discounted price of an item

        Args:
            price (float): The original price of the item
            discount_percentage (float): The discount percentage

        Returns:
            float: The discounted price of the item
        """
        discount = MathOperations.multiply(price, MathOperations.divide(discount_percentage, 100))
        return MathOperations.subtract(price, discount)

    @service_method
    async def get(self, id: int):
        """
        Get an item by ID

        Args:
            id (int): The ID of the item

        Returns:
            Item: The item with the specified ID

        Raises:
            HTTPException: If the item is not found
        """
        item = self.uow.item_repository.get_by_id(id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {id} not found"
            )
        return item

    @service_method
    async def create(self, item: Item):
        """
        Create a new item

        Args:
            item (Item): The item to create

        Returns:
            Item: The created item
        """
        return self.uow.item_repository.add(item)

    @service_method
    async def update(self, item: Item):
        """
        Update an existing item

        Args:
            item (Item): The item to update

        Returns:
            Item: The updated item
        """
        return self.uow.item_repository.update(item)

    @service_method
    async def delete(self, id: int):
        """
        Delete an item by ID

        Args:
            id (int): The ID of the item to delete

        Returns:
            None
        """
        item = self.uow.item_repository.get_by_id(id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {id} not found"
            )
        self.uow.item_repository.soft_delete(item)

    @staticmethod
    def get_self(db: Session = Depends(get_db)):
        """
        Get the item service instance

        Args:
            db (Session): The database session, injected by FastAPI

        Returns:
            ItemService: The item service instance
        """
        uow = UnitOfWork(db)
        return ItemService(uow)
