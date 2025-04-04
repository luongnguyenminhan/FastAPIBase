"""
Math Controller

This file defines the MathController class for handling math operation endpoints.
It follows the controller pattern to separate route definition from request handling logic.

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.1.0
"""

from typing import List, Dict, Any

from app.db.base import get_db
from app.schemas.business_model.response_base import BaseResponseModel, SuccessResponseModel
from app.schemas.view_model.response import OperationResultViewModel
from app.services.services.math_service import MathService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


class MathController:
    """
    Controller handling math-related endpoints including various operations
    like add, subtract, multiply, etc.
    """

    def __init__(self, router: APIRouter, db: Session = Depends(get_db)):
        """
        Initialize the controller with router and database session.
        
        Args:
            router: FastAPI router instance
            db: Database session
        """
        self.router = router
        self.math_service = MathService.get_self(db)
        self._register_routes()

    def _register_routes(self) -> None:
        """Register all math routes with the router."""
        self.router.add_api_route(
            "/calculate/{operation}",
            self.calculate_operation,
            methods=["POST"],
            response_model=BaseResponseModel[float],
            summary="Calculate operation",
            description="Perform a mathematical operation on two numbers",
            operation_id="calculate_operation_v1"
        )

        self.router.add_api_route(
            "/operations",
            self.get_available_operations,
            methods=["GET"],
            response_model=BaseResponseModel[List[str]],
            summary="Available operations",
            description="Get a list of available mathematical operations",
            operation_id="get_available_operations_v1"
        )

        self.router.add_api_route(
            "/batch",
            self.calculate_multiple_operations,
            methods=["POST"],
            response_model=BaseResponseModel[List[OperationResultViewModel]],
            summary="Batch calculate",
            description="Perform multiple mathematical operations in a single request",
            operation_id="calculate_multiple_operations_v1"
        )

    async def calculate_operation(
            self,
            operation: str,
            x: float,
            y: float
    ) -> SuccessResponseModel:
        """
        Calculate a mathematical operation.
        
        Args:
            operation: The operation to perform (add, subtract, etc.)
            x: The first operand
            y: The second operand
            
        Returns:
            SuccessResponseModel: The calculation result
        """
        result = await self.math_service.calculate_operation(operation, x, y)
        return SuccessResponseModel(
            message=f"Operation '{operation}' calculated successfully",
            data=result
        )

    async def get_available_operations(
            self
    ) -> SuccessResponseModel:
        """
        Get a list of available mathematical operations.
            
        Returns:
            SuccessResponseModel: The list of available operations
        """
        operations = await self.math_service.get_available_operations()
        return SuccessResponseModel(
            message="Available operations retrieved successfully",
            data=operations
        )

    async def calculate_multiple_operations(
            self,
            operations: List[Dict[str, Any]]
    ) -> SuccessResponseModel:
        """
        Calculate multiple operations in a batch.
        
        Args:
            operations: List of operations with operation name and operands
            
        Returns:
            SuccessResponseModel: The results of all operations
        """
        results = await self.math_service.calculate_multiple_operations(operations)

        # Create a list of result view models
        result_view_models = []
        for i, op_data in enumerate(operations):
            result_view_models.append(
                OperationResultViewModel(
                    operation=op_data.get('operation', ''),
                    x=op_data.get('x', 0.0),
                    y=op_data.get('y', 0.0),
                    result=results[i]
                )
            )

        return SuccessResponseModel(
            message=f"Successfully calculated {len(results)} operations",
            data=result_view_models
        )
