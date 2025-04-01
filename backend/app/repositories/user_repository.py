"""
User Repository Implementation

This file defines the UserRepository class for managing user-related database operations.
It inherits from BaseRepository and provides additional methods specific to users.

Dependencies:
- SQLAlchemy for database operations
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

import logging
from typing import List, Optional, Type

from app.db.models import User
from app.repositories.repository_interface.i_user_repository import IUserRepository
from sqlalchemy.orm import Session

from .base_repository import BaseRepository

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[User], IUserRepository):
    """
    Repository class for managing users

    Attributes:
        db (Session): The database session
    """

    def __init__(self, db: Session):
        """
        Initialize the user repository with a database session

        Args:
            db (Session): The database session
        """
        super().__init__(User, db)
        logger.info("UserRepository initialized")

    @property
    def model(self) -> Type[User]:
        """Get the model class"""
        return User

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email

        Args:
            email (str): The email of the user

        Returns:
            Optional[User]: The user with the specified email or None if not found
        """
        logger.debug(f"Getting user by email: {email}")
        return self._dbSet.filter_by(email=email, is_deleted=False).first()

    def get_active_users(self) -> List[User]:
        """
        Get all active users

        Returns:
            List[User]: A list of active users
        """
        logger.debug("Getting all active users")
        return self._dbSet.filter_by(is_active=True, is_deleted=False).all()
