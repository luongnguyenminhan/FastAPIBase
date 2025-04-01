"""
User Service Interface Definition

This file defines the service interface for managing user-related business logic.
It inherits from IBaseService and defines the interface for user service implementations.

Dependencies:
- FastAPI for dependency injection
- SQLAlchemy for database operations

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.0.0
"""

from abc import abstractmethod
from typing import List, Dict, Optional, Union

from app.db.models import User
from app.db.models.items import Item
from app.services.service_interface.i_base_service import IBaseService


class IUserService(IBaseService[User]):
    """Interface for user service operations"""

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        pass

    @abstractmethod
    async def get_active_users(self) -> List[User]:
        """Get all active users"""
        pass

    @abstractmethod
    async def get_user_items(self, user_id: int) -> List[Item]:
        """Get items owned by a user"""
        pass

    @abstractmethod
    async def calculate_user_metrics(self, metric_values: List[float]) -> Dict[str, Union[float, int]]:
        """Calculate user metrics"""
        pass

    @abstractmethod
    async def get(self, id: int) -> User:
        """Get a user by ID"""
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user"""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user"""
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        """Delete a user by ID"""
        pass
