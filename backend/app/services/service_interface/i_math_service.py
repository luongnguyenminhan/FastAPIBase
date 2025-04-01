"""
Math Service Interface Definition

This file defines the service interface for performing mathematical operations.
It inherits from IBaseService and defines the interface for math service implementations.

Dependencies:
- FastAPI for dependency injection
- SQLAlchemy for database operations

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.0.0
"""

from abc import abstractmethod
from typing import List, Dict, Any

from app.services.service_interface.i_base_service import IBaseService


class IMathService(IBaseService[Any]):
    """Interface for math service operations"""

    @abstractmethod
    async def calculate_operation(self, operation: str, x: float, y: float) -> float:
        """Perform a mathematical operation"""
        pass

    @abstractmethod
    async def get_available_operations(self) -> List[str]:
        """Get a list of available mathematical operations"""
        pass

    @abstractmethod
    async def calculate_multiple_operations(self, operations: List[Dict[str, Any]]) -> List[float]:
        """Perform multiple mathematical operations"""
        pass
