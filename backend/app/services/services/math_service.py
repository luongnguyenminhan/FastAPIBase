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
Last Modified: 23 Jun 2024
Version: 1.0.0
"""

from typing import Dict, Callable, Any, List, Optional, Dict, Union
import logging
from app.unit_of_work.unit_of_work import UnitOfWork
from app.services.utils.example_core import MathOperations
from .base_service import service_method, BaseService
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.utils.exceptions.exceptions import (
    BadRequestException,
    InternalServerException
)

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
            BadRequestException: If the operation is not supported or if there's a calculation error
        """
        logger.debug(f"Calculating operation: {operation} with x={x}, y={y}")
        
        if operation not in self.operations:
            logger.warning(f"Unsupported operation requested: {operation}")
            raise BadRequestException(
                error_code="UNSUPPORTED_OPERATION",
                message=f"Unsupported operation: {operation}"
            )
        
        try:
            result: float = self.operations[operation](x, y)
            logger.debug(f"Operation result: {result}")
            return result
        except ZeroDivisionError:
            logger.error(f"Division by zero error in operation {operation} with x={x}, y={y}")
            raise BadRequestException(
                error_code="DIVISION_BY_ZERO",
                message="Division by zero is not allowed"
            )
        except Exception as e:
            logger.error(f"Error in operation {operation} with x={x}, y={y}: {str(e)}")
            raise InternalServerException(
                error_code="CALCULATION_ERROR",
                message=f"Error performing operation: {str(e)}"
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
            BadRequestException: If any operation is not supported or if the input is invalid
        """
        logger.debug(f"Calculating multiple operations: {len(operations)} operations")
        
        if not operations:
            logger.warning("Empty operations list provided")
            raise BadRequestException(
                error_code="EMPTY_OPERATIONS_LIST",
                message="Cannot process empty operations list"
            )
            
        results: List[float] = []
        
        for i, op_data in enumerate(operations):
            if not isinstance(op_data, dict):
                logger.error(f"Invalid operation data format at index {i}")
                raise BadRequestException(
                    error_code="INVALID_OPERATION_FORMAT",
                    message=f"Operation at index {i} has invalid format"
                )
                
            operation: str = op_data.get('operation', '')
            if not operation:
                logger.error(f"Missing operation name at index {i}")
                raise BadRequestException(
                    error_code="MISSING_OPERATION_NAME",
                    message=f"Operation name is missing at index {i}"
                )
                
            x: float = op_data.get('x', 0.0)
            y: float = op_data.get('y', 0.0)
            
            result = await self.calculate_operation(operation, x, y)
            results.append(result)
            
        return results
