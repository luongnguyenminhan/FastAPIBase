"""
User Service Implementation

This file defines the UserService class, which provides methods for managing users.
It inherits from BaseService and uses the Unit of Work pattern for transaction management.

Dependencies:
- FastAPI for dependency injection and HTTP exceptions
- SQLAlchemy for database operations
- Unit of Work pattern for transaction management
- Repository pattern for data access

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from .base_service import BaseService, service_method
from app.db.models import User
from app.repositories.user_repository import UserRepository
from app.unit_of_work.unit_of_work import UnitOfWork
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db

class UserService(BaseService[User]):
    """
    Service class for managing users

    Attributes:
        uow (UnitOfWork): The Unit of Work instance for managing transactions
    """

    def __init__(self, uow: UnitOfWork):
        """
        Initialize the user service with a Unit of Work

        Args:
            uow (UnitOfWork): The Unit of Work instance for managing transactions
        """
        super().__init__(uow)

    @staticmethod
    def get_self(db: Session = Depends(get_db)):
        """
        Get the user service instance

        Args:
            db (Session): The database session, injected by FastAPI

        Returns:
            UserService: The user service instance
        """
        uow = UnitOfWork(db)
        return UserService(uow)

    @service_method
    async def get_by_email(self, email: str):
        """
        Get a user by email

        Args:
            email (str): The email of the user

        Returns:
            User: The user with the specified email
        """
        return self.uow.user_repository.get_by_email(email)

    @service_method
    async def get_active_users(self):
        """
        Get all active users

        Returns:
            List[User]: A list of active users
        """
        return self.uow.user_repository.get_active_users()

    @service_method
    async def get_user_items(self, user_id: int):
        """
        Get items owned by a user

        Args:
            user_id (int): The ID of the user

        Returns:
            List[Item]: A list of items owned by the user
        """
        return self.uow.item_repository.get_by_owner(user_id)

    @service_method
    async def calculate_user_metrics(self, metric_values: list[float]) -> dict:
        """
        Calculate user metrics

        Args:
            metric_values (list[float]): A list of metric values

        Returns:
            dict: A dictionary containing the total and average of the metric values
        """
        if not metric_values:
            return {"total": 0, "average": 0}
        total = sum(metric_values)
        average = total / len(metric_values)
        return {"total": total, "average": average}

    @service_method
    async def get(self, id: int):
        """
        Get a user by ID

        Args:
            id (int): The ID of the user

        Returns:
            User: The user with the specified ID

        Raises:
            HTTPException: If the user is not found
        """
        user = self.uow.user_repository.get_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {id} not found"
            )
        return user
