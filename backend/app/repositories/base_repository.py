"""
Base Repository Implementation

This file defines the base repository class for managing database operations.
It provides a consistent interface for CRUD operations and pagination.

Dependencies:
- SQLAlchemy for database operations
- Pydantic for data validation and serialization

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, List
from sqlalchemy.future import select
from datetime import datetime
from app.schemas.common import PaginationParameter, Pagination
from app.db.models.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseRepository(Generic[T]):
    """
    Base repository class for managing database operations

    Attributes:
        model (Type[T]): The model class
        db (Session): The database session
        _dbSet: The query object for the model
    """

    def __init__(self, model: Type[T], db: Session):
        """
        Initialize the base repository with a model and database session

        Args:
            model (Type[T]): The model class
            db (Session): The database session
        """
        self.model = model
        self.db = db
        self._dbSet = db.query(model)

    def get_by_id(self, id: int) -> T:
        """
        Get an entity by ID

        Args:
            id (int): The ID of the entity

        Returns:
            T: The entity with the specified ID
        """
        return self._dbSet.filter_by(id=id, is_deleted=False).first()

    def get_all(self) -> List[T]:
        """
        Get all entities

        Returns:
            List[T]: A list of all entities
        """
        return self._dbSet.filter_by(is_deleted=False).all()

    def add(self, entity: T) -> T:
        """
        Add a new entity

        Args:
            entity (T): The entity to add

        Returns:
            T: The added entity
        """
        entity.create_date = datetime.utcnow()
        self.db.add(entity)
        self.db.flush()
        return entity

    def add_range(self, entities: List[T]):
        """
        Add a range of entities

        Args:
            entities (List[T]): The list of entities to add
        """
        current_time = datetime.utcnow()
        for entity in entities:
            entity.create_date = current_time
        self.db.add_all(entities)
        self.db.flush()

    def update(self, entity: T):
        """
        Update an existing entity

        Args:
            entity (T): The entity to update
        """
        entity.update_date = datetime.utcnow()
        self._dbSet.update(entity)

    def soft_delete(self, entity: T):
        """
        Soft delete an entity

        Args:
            entity (T): The entity to soft delete
        """
        entity.is_deleted = True
        self._dbSet.update(entity)

    def soft_delete_range(self, entities: List[T]):
        """
        Soft delete a range of entities

        Args:
            entities (List[T]): The list of entities to soft delete
        """
        for entity in entities:
            entity.is_deleted = True
        self._dbSet.update(entities)

    def permanent_delete(self, entity: T):
        """
        Permanently delete an entity

        Args:
            entity (T): The entity to permanently delete
        """
        self.db.delete(entity)

    def permanent_delete_list(self, entities: List[T]):
        """
        Permanently delete a list of entities

        Args:
            entities (List[T]): The list of entities to permanently delete
        """
        for entity in entities:
            self.db.delete(entity)

    def to_pagination(self, pagination_parameter: PaginationParameter) -> Pagination[T]:
        """
        Convert query results to paginated results

        Args:
            pagination_parameter (PaginationParameter): The pagination parameters

        Returns:
            Pagination[T]: The paginated results
        """
        query = self._dbSet.filter_by(is_deleted=False)

        # Get total count
        total_count = query.count()

        # Get paginated items
        items = query.offset(
            (pagination_parameter.page_index - 1) * pagination_parameter.page_size
        ).limit(pagination_parameter.page_size).all()

        return Pagination(
            items=items,
            total_count=total_count,
            page_index=pagination_parameter.page_index,
            page_size=pagination_parameter.page_size
        )
