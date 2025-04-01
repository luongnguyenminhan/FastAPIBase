"""
Base Service Implementation

This file defines the base service class and a decorator for handling service methods.
It provides:
- A base class for all services to inherit from
- A decorator for handling exceptions in service methods
- Dependency injection for Unit of Work and repositories

The BaseService class is a generic class that requires a repository type to be specified
by subclasses. It provides a consistent interface for accessing repositories and managing
transactions.

Dependencies:
- FastAPI for dependency injection and HTTP exceptions
- SQLAlchemy for database operations
- Unit of Work pattern for transaction management
- Repository pattern for data access

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from abc import abstractmethod
from typing import Generic, TypeVar, Callable, Type, Any, Optional, TypedDict, cast
from functools import wraps
import logging
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.unit_of_work.unit_of_work import UnitOfWork
from app.repositories.base_repository import BaseRepository
from app.db.base import get_db

T = TypeVar('T')
logger = logging.getLogger(__name__)


class ServiceResponse(TypedDict, total=False):
    """Type for standardized service responses"""
    success: bool
    data: Any
    message: Optional[str]
    error: Optional[str]


def service_method(func: Callable) -> Callable:
    """
    Decorator for service methods to handle exceptions

    Args:
        func (Callable): The service method to be decorated

    Returns:
        Callable: The wrapped service method with exception handling
    """
    @wraps(func)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            logger.debug(f"Executing service method: {func.__name__}")
            result = await func(self, *args, **kwargs)
            logger.debug(f"Completed service method: {func.__name__}")
            return result
        except HTTPException as he:
            logger.error(f"HTTP exception in {func.__name__}: {he.detail}")
            raise he
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    return wrapper


class BaseService(Generic[T]):
    """
    Base service class for managing repositories and transactions

    Attributes:
        repository_type (Type[BaseRepository]): The type of repository to be used by the service
        uow (UnitOfWork): The Unit of Work instance for managing transactions
    """
    repository_type: Type[BaseRepository] = None  # Subclasses must set this

    def __init__(self, uow: UnitOfWork):
        """
        Initialize the base service with a Unit of Work

        Args:
            uow (UnitOfWork): The Unit of Work instance for managing transactions
        """
        self.uow: UnitOfWork = uow
        logger.info(f"Initialized {self.__class__.__name__}")

    @staticmethod
    @abstractmethod
    def get_self(db: Session = Depends(get_db)) -> 'BaseService[T]':
        """
        Abstract method to get the service instance

        Args:
            db (Session): The database session, injected by FastAPI

        Returns:
            BaseService: The service instance

        Raises:
            NotImplementedError: If the method is not implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def create_response(self, 
                        success: bool = True, 
                        data: Any = None, 
                        message: Optional[str] = None, 
                        error: Optional[str] = None) -> ServiceResponse:
        """
        Create a standardized service response

        Args:
            success (bool): Whether the operation was successful
            data (Any): The data to return
            message (Optional[str]): A success message
            error (Optional[str]): An error message

        Returns:
            ServiceResponse: A standardized service response
        """
        response: ServiceResponse = {"success": success}
        
        if data is not None:
            response["data"] = data
        
        if message is not None:
            response["message"] = message
            
        if error is not None:
            response["error"] = error
            
        return response
