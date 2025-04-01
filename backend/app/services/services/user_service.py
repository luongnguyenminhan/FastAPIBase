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
Last Modified: 23 Jun 2024
Version: 1.0.0
"""

from typing import List, Dict, Optional, Any, Union
import logging
from .base_service import BaseService, service_method, ServiceResponse
from app.db.models import User
from app.db.models.items import Item
from app.repositories.user_repository import UserRepository
from app.unit_of_work.unit_of_work import UnitOfWork
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.utils.exceptions.exceptions import (
    NotFoundException, 
    BadRequestException,
    InternalServerException
)

logger = logging.getLogger(__name__)


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
        logger.info("UserService initialized")

    @staticmethod
    def get_self(db: Session = Depends(get_db)) -> 'UserService':
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
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email

        Args:
            email (str): The email of the user

        Returns:
            Optional[User]: The user with the specified email or None if not found
        """
        logger.debug(f"Getting user by email: {email}")
        user = self.uow.user_repository.get_by_email(email)
        if not user:
            logger.warning(f"User with email {email} not found")
            raise NotFoundException(
                error_code="USER_EMAIL_NOT_FOUND",
                message=f"User with email {email} not found"
            )
        return user

    @service_method
    async def get_active_users(self) -> List[User]:
        """
        Get all active users

        Returns:
            List[User]: A list of active users
        """
        logger.debug("Getting all active users")
        return self.uow.user_repository.get_active_users()

    @service_method
    async def get_user_items(self, user_id: int) -> List[Item]:
        """
        Get items owned by a user

        Args:
            user_id (int): The ID of the user

        Returns:
            List[Item]: A list of items owned by the user
            
        Raises:
            NotFoundException: If the user is not found
        """
        logger.debug(f"Getting items for user ID: {user_id}")
        user = self.uow.user_repository.get_by_id(user_id)
        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise NotFoundException(
                error_code="USER_NOT_FOUND",
                message=f"User with id {user_id} not found"
            )
        return self.uow.item_repository.get_by_owner(user_id)

    @service_method
    async def calculate_user_metrics(self, metric_values: List[float]) -> Dict[str, Union[float, int]]:
        """
        Calculate user metrics

        Args:
            metric_values (List[float]): A list of metric values

        Returns:
            Dict[str, Union[float, int]]: A dictionary containing the total and average of the metric values
            
        Raises:
            BadRequestException: If the metric values list is empty
        """
        logger.debug(f"Calculating metrics for {len(metric_values)} values")
        if not metric_values:
            logger.warning("Empty metric values list provided")
            raise BadRequestException(
                error_code="EMPTY_METRICS",
                message="Cannot calculate metrics with empty values list"
            )
        
        try:
            total: float = sum(metric_values)
            average: float = total / len(metric_values)
            return {"total": total, "average": average}
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            raise InternalServerException(
                error_code="METRICS_CALCULATION_ERROR",
                message=f"Failed to calculate metrics: {str(e)}"
            )

    @service_method
    async def get(self, id: int) -> User:
        """
        Get a user by ID

        Args:
            id (int): The ID of the user

        Returns:
            User: The user with the specified ID

        Raises:
            NotFoundException: If the user is not found
        """
        logger.debug(f"Getting user by ID: {id}")
        user: Optional[User] = self.uow.user_repository.get_by_id(id)
        if not user:
            logger.warning(f"User with ID {id} not found")
            raise NotFoundException(
                error_code="USER_NOT_FOUND",
                message=f"User with id {id} not found"
            )
        return user

    @service_method
    async def create(self, user: User) -> User:
        """
        Create a new user

        Args:
            user (User): The user to create

        Returns:
            User: The created user
        """
        try:
            logger.info(f"Creating new user with email: {user.email}")
            # Check if user with email already exists
            existing_user = self.uow.user_repository.get_by_email(user.email)
            if existing_user:
                logger.warning(f"User with email {user.email} already exists")
                raise BadRequestException(
                    error_code="EMAIL_ALREADY_EXISTS",
                    message=f"User with email {user.email} already exists"
                )
                
            with self.uow:
                created_user: User = self.uow.user_repository.add(user)
                self.uow.commit()
            logger.info(f"Created user with ID: {created_user.id}")
            return created_user
        except BadRequestException:
            raise
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            self.uow.rollback()
            raise InternalServerException(
                error_code="USER_CREATION_ERROR",
                message=f"Failed to create user: {str(e)}"
            )

    @service_method
    async def update(self, user: User) -> User:
        """
        Update an existing user

        Args:
            user (User): The user to update

        Returns:
            User: The updated user
        """
        try:
            logger.info(f"Updating user with ID: {user.id}")
            with self.uow:
                existing_user: Optional[User] = self.uow.user_repository.get_by_id(user.id)
                if not existing_user:
                    logger.warning(f"User with ID {user.id} not found for update")
                    raise NotFoundException(
                        error_code="USER_NOT_FOUND",
                        message=f"User with id {user.id} not found"
                    )
                
                self.uow.user_repository.update(user)
                self.uow.commit()
            logger.info(f"Updated user with ID: {user.id}")
            return user
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            self.uow.rollback()
            raise InternalServerException(
                error_code="USER_UPDATE_ERROR",
                message=f"Failed to update user: {str(e)}"
            )

    @service_method
    async def delete(self, id: int) -> None:
        """
        Delete a user by ID

        Args:
            id (int): The ID of the user to delete

        Returns:
            None

        Raises:
            NotFoundException: If the user is not found
        """
        try:
            logger.info(f"Deleting user with ID: {id}")
            with self.uow:
                user: Optional[User] = self.uow.user_repository.get_by_id(id)
                if not user:
                    logger.warning(f"User with ID {id} not found for deletion")
                    raise NotFoundException(
                        error_code="USER_NOT_FOUND",
                        message=f"User with id {id} not found"
                    )
                
                self.uow.user_repository.soft_delete(user)
                self.uow.commit()
            logger.info(f"Deleted user with ID: {id}")
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            self.uow.rollback()
            raise InternalServerException(
                error_code="USER_DELETION_ERROR",
                message=f"Failed to delete user: {str(e)}"
            )
