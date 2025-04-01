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
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.future import select
from datetime import datetime
import logging
from app.schemas.business_model.common import PaginationParameterModel, PaginatedResultModel
from app.db.models.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)
logger = logging.getLogger(__name__)


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
        self.model: Type[T] = model
        self.db: Session = db
        self._dbSet = db.query(model)
        logger.info(f"Initialized {self.__class__.__name__} for model {model.__name__}")

    def get_by_id(self, id: int) -> Optional[T]:
        """
        Get an entity by ID

        Args:
            id (int): The ID of the entity

        Returns:
            Optional[T]: The entity with the specified ID or None if not found
        """
        logger.debug(f"Getting {self.model.__name__} by id: {id}")
        return self._dbSet.filter_by(id=id, is_deleted=False).first()

    def get_all(self) -> List[T]:
        """
        Get all entities

        Returns:
            List[T]: A list of all entities
        """
        logger.debug(f"Getting all {self.model.__name__} entities")
        return self._dbSet.filter_by(is_deleted=False).all()

    def add(self, entity: T) -> T:
        """
        Add a new entity

        Args:
            entity (T): The entity to add

        Returns:
            T: The added entity
        """
        try:
            entity.create_date = datetime.utcnow()
            self.db.add(entity)
            self.db.flush()
            logger.info(f"Added new {self.model.__name__} with id: {entity.id}")
            return entity
        except Exception as e:
            logger.error(f"Error adding {self.model.__name__}: {str(e)}")
            raise

    def add_range(self, entities: List[T]) -> None:
        """
        Add a range of entities

        Args:
            entities (List[T]): The list of entities to add
        """
        try:
            current_time: datetime = datetime.utcnow()
            for entity in entities:
                entity.create_date = current_time
            self.db.add_all(entities)
            self.db.flush()
            logger.info(f"Added {len(entities)} {self.model.__name__} entities")
        except Exception as e:
            logger.error(f"Error adding range of {self.model.__name__}: {str(e)}")
            raise

    def update(self, entity: T) -> None:
        """
        Update an existing entity

        Args:
            entity (T): The entity to update
        """
        try:
            entity.update_date = datetime.utcnow()
            self.db.merge(entity)
            self.db.flush()
            logger.info(f"Updated {self.model.__name__} with id: {entity.id}")
        except Exception as e:
            logger.error(f"Error updating {self.model.__name__}: {str(e)}")
            raise

    def soft_delete(self, entity: T) -> None:
        """
        Soft delete an entity

        Args:
            entity (T): The entity to soft delete
        """
        try:
            entity.is_deleted = True
            entity.update_date = datetime.utcnow()
            self.db.merge(entity)
            self.db.flush()
            logger.info(f"Soft deleted {self.model.__name__} with id: {entity.id}")
        except Exception as e:
            logger.error(f"Error soft deleting {self.model.__name__}: {str(e)}")
            raise

    def soft_delete_range(self, entities: List[T]) -> None:
        """
        Soft delete a range of entities

        Args:
            entities (List[T]): The list of entities to soft delete
        """
        try:
            current_time: datetime = datetime.utcnow()
            for entity in entities:
                entity.is_deleted = True
                entity.update_date = current_time
            
            for entity in entities:
                self.db.merge(entity)
            self.db.flush()
            logger.info(f"Soft deleted {len(entities)} {self.model.__name__} entities")
        except Exception as e:
            logger.error(f"Error soft deleting range of {self.model.__name__}: {str(e)}")
            raise

    def permanent_delete(self, entity: T) -> None:
        """
        Permanently delete an entity

        Args:
            entity (T): The entity to permanently delete
        """
        try:
            self.db.delete(entity)
            self.db.flush()
            logger.info(f"Permanently deleted {self.model.__name__} with id: {entity.id}")
        except Exception as e:
            logger.error(f"Error permanently deleting {self.model.__name__}: {str(e)}")
            raise

    def permanent_delete_list(self, entities: List[T]) -> None:
        """
        Permanently delete a list of entities

        Args:
            entities (List[T]): The list of entities to permanently delete
        """
        try:
            for entity in entities:
                self.db.delete(entity)
            self.db.flush()
            logger.info(f"Permanently deleted {len(entities)} {self.model.__name__} entities")
        except Exception as e:
            logger.error(f"Error permanently deleting list of {self.model.__name__}: {str(e)}")
            raise

    def to_pagination(self, pagination_parameter: PaginationParameterModel) -> PaginatedResultModel[T]:
        """
        Convert query results to paginated results

        Args:
            pagination_parameter (PaginationParameterModel): The pagination parameters

        Returns:
            PaginatedResultModel[T]: The paginated results
        """
        try:
            query = self._dbSet.filter_by(is_deleted=False)

            # Get total count
            total_count: int = query.count()

            # Get paginated items
            items: List[T] = query.offset(
                (pagination_parameter.page_index - 1) * pagination_parameter.page_size
            ).limit(pagination_parameter.page_size).all()

            logger.debug(f"Paginated {self.model.__name__} results: page {pagination_parameter.page_index}, count {len(items)}, total {total_count}")
            
            return PaginatedResultModel(
                items=items,
                total_count=total_count,
                page_index=pagination_parameter.page_index,
                page_size=pagination_parameter.page_size
            )
        except Exception as e:
            logger.error(f"Error paginating {self.model.__name__}: {str(e)}")
            raise
