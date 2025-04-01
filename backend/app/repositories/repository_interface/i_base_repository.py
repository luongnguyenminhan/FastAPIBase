"""
Repository Interface Definition

This file defines the repository interface for managing database operations.
It provides a consistent interface for CRUD operations and pagination.

Dependencies:
- SQLAlchemy for database operations types
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: Current Date
Version: 1.0.0
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, List, Optional

from app.db.models.base_model import BaseModel
from app.schemas.business_model.common import PaginationParameterModel, PaginatedResultModel

T = TypeVar('T', bound=BaseModel)


class IRepository(Generic[T], ABC):
    """Repository interface for managing database operations"""

    @property
    @abstractmethod
    def model(self) -> Type[T]:
        """Get the model class"""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Get an entity by ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities"""
        pass

    @abstractmethod
    def add(self, entity: T) -> T:
        """Add a new entity"""
        pass

    @abstractmethod
    def add_range(self, entities: List[T]) -> None:
        """Add a range of entities"""
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        """Update an existing entity"""
        pass

    @abstractmethod
    def soft_delete(self, entity: T) -> None:
        """Soft delete an entity"""
        pass

    @abstractmethod
    def soft_delete_range(self, entities: List[T]) -> None:
        """Soft delete a range of entities"""
        pass

    @abstractmethod
    def permanent_delete(self, entity: T) -> None:
        """Permanently delete an entity"""
        pass

    @abstractmethod
    def permanent_delete_list(self, entities: List[T]) -> None:
        """Permanently delete a list of entities"""
        pass

    @abstractmethod
    def to_pagination(self, pagination_parameter: PaginationParameterModel) -> PaginatedResultModel[T]:
        """Convert query results to paginated results"""
        pass
