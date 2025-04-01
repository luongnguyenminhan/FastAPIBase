"""
User Repository Interface

This file defines the UserRepositoryInterface for managing user-related database operations.
It inherits from IRepository and defines the interface for user repository implementations.

Dependencies:
- SQLAlchemy for database operations
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 2024
Version: 1.0.0
"""

from abc import abstractmethod
from typing import List, Optional

from app.db.models import User

from .i_base_repository import IRepository


class IUserRepository(IRepository[User]):
    """Repository interface for managing users"""

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        pass

    @abstractmethod
    def get_active_users(self) -> List[User]:
        """Get all active users"""
        pass
