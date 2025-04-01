"""
Math Service Implementation

This file defines the MathService class, which provides methods for performing mathematical operations.
It uses the Unit of Work pattern for transaction management and a utility class for math operations.

Dependencies:
- FastAPI for dependency injection and HTTP exceptions
- SQLAlchemy for database operations
- Unit of Work pattern for transaction management
- MathOperations utility class for performing calculations

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from typing import Dict, Callable, Any, List, Optional, Dict, Union
import logging
from app.unit_of_work.unit_of_work import UnitOfWork
from app.services.utils.example_core import MathOperations
from .base_service import service_method, BaseService
from fastapi import HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.base import get_db

logger = logging.getLogger(__name__)


class MathService(BaseService[Any]):
    """
    Service class for performing mathematical operations

    Attributes:
        uow (UnitOfWork): The Unit of Work instance for managing transactions
        operations (Dict[str, Callable[[float, float], float]]): A dictionary mapping operation names to functions
    """

    def __init__(self, uow: UnitOfWork):
        """
        Initialize the math service with a Unit of Work

        Args:
            uow (UnitOfWork): The Unit of Work instance for managing transactions
        """
        super().__init__(uow)
        self.operations: Dict[str, Callable[[float, float], float]] = {
            'add': MathOperations.add,
            'subtract': MathOperations.subtract,
            'multiply': MathOperations.multiply,
            'divide': MathOperations.divide,
            'power': MathOperations.power
        }
        logger.info("MathService initialized")

    @staticmethod
    def get_self(db: Session = Depends(get_db)) -> 'MathService':
        """
        Get the math service instance

        Args:
            db (Session): The database session, injected by FastAPI

        Returns:
            MathService: The math service instance
        """
        uow = UnitOfWork(db)
        return MathService(uow)

    @service_method
    async def calculate_operation(self, operation: str, x: float, y: float) -> float:
        """
        Perform a mathematical operation

        Args:
            operation (str): The name of the operation to perform
            x (float): The first operand
            y (float): The second operand

        Returns:
            float: The result of the operation

        Raises:
            HTTPException: If the operation is not supported
        """
        logger.debug(f"Calculating operation: {operation} with x={x}, y={y}")
        
        if operation not in self.operations:
            logger.warning(f"Unsupported operation requested: {operation}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported operation: {operation}"
            )
        
        try:
            result: float = self.operations[operation](x, y)
            logger.debug(f"Operation result: {result}")
            return result
        except ZeroDivisionError:
            logger.error(f"Division by zero error in operation {operation} with x={x}, y={y}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Division by zero is not allowed"
            )
        except Exception as e:
            logger.error(f"Error in operation {operation} with x={x}, y={y}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error performing operation: {str(e)}"
            )
    
    @service_method
    async def get_available_operations(self) -> List[str]:
        """
        Get a list of available mathematical operations

        Returns:
            List[str]: A list of available operation names
        """
        logger.debug("Getting available operations")
        return list(self.operations.keys())
    
    @service_method
    async def calculate_multiple_operations(self, operations: List[Dict[str, Any]]) -> List[float]:
        """
        Perform multiple mathematical operations

        Args:
            operations (List[Dict[str, Any]]): A list of operations, each with 'operation', 'x', and 'y' keys

        Returns:
            List[float]: A list of results for each operation

        Raises:
            HTTPException: If any operation is not supported
        """
        logger.debug(f"Calculating multiple operations: {len(operations)} operations")
        results: List[float] = []
        
        for op_data in operations:
            operation: str = op_data.get('operation', '')
            x: float = op_data.get('x', 0.0)
            y: float = op_data.get('y', 0.0)
            
            result = await self.calculate_operation(operation, x, y)
            results.append(result)
            
        return results
