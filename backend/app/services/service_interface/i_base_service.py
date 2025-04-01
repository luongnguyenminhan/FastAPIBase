"""
Base Service Interface Definition

This file defines the service interface for managing business logic operations.
It provides a consistent interface for service operations.

Dependencies:
- FastAPI for dependency injection
- SQLAlchemy for database operations

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.0.0
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Optional, TypedDict

from app.db.base import get_db
from app.db.models.base_model import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session

T = TypeVar('T', bound=BaseModel)


class ServiceResponse(TypedDict, total=False):
    """Type for standardized service responses"""
    success: bool
    data: Any
    message: Optional[str]
    error: Optional[str]


class IBaseService(Generic[T], ABC):
    """Interface for base service operations"""

    @staticmethod
    @abstractmethod
    def get_self(db: Session = Depends(get_db)) -> 'IBaseService[T]':
        """Get the service instance"""
        pass

    @abstractmethod
    def create_response(self,
                        success: bool = True,
                        data: Any = None,
                        message: Optional[str] = None,
                        error: Optional[str] = None) -> ServiceResponse:
        """Create a standardized service response"""
        pass
