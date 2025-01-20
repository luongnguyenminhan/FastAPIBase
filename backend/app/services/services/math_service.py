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

from app.unit_of_work.unit_of_work import UnitOfWork
from app.services.utils.example_core import MathOperations
from .base_service import service_method
from fastapi import HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.base import get_db


class MathService:
    """
    Service class for performing mathematical operations

    Attributes:
        uow (UnitOfWork): The Unit of Work instance for managing transactions
        operations (dict): A dictionary mapping operation names to functions
    """

    def __init__(self, uow: UnitOfWork):
        """
        Initialize the math service with a Unit of Work

        Args:
            uow (UnitOfWork): The Unit of Work instance for managing transactions
        """
        self.uow = uow
        self.operations = {
            'add': MathOperations.add,
            'subtract': MathOperations.subtract,
            'multiply': MathOperations.multiply,
            'divide': MathOperations.divide,
            'power': MathOperations.power
        }

    @staticmethod
    def get_self(db: Session = Depends(get_db)):
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
        if operation not in self.operations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported operation: {operation}"
            )
        return self.operations[operation](x, y)
