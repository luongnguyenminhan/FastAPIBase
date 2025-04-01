"""
Math Controller

This file defines the MathController class for handling math-related endpoints.
It follows the controller pattern to separate route definition from request handling logic.

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.1.0
"""

from fastapi import APIRouter, Depends
from app.services.services.math_service import MathService
from app.schemas.view_model.request import MathOperationViewModel
from app.schemas.common import BaseResponseModel, SuccessResponseModel


class MathController:
    """
    Controller handling math-related endpoints for various calculations.
    """
    
    def __init__(self, router: APIRouter):
        self.router = router
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register all math routes with the router."""
        self.router.add_api_route(
            "/{operation}",
            self.calculate,
            methods=["POST"],
            response_model=BaseResponseModel[float],
            summary="Perform math operation",
            description="Calculate result of specified operation with two operands",
            operation_id="calculate_math_v1"
        )
    
    async def calculate(
        self,
        operation: str,
        request: MathOperationViewModel,
        math_service: MathService = Depends(MathService.get_self)
    ) -> SuccessResponseModel:
        """
        Perform a math operation.
        
        Args:
            operation: The operation to perform (add, subtract, multiply, divide, power)
            request: The request containing operands
            math_service: The math service for business logic
            
        Returns:
            SuccessResponseModel: The calculation result
        """
        result = await math_service.calculate_operation(operation, request.x, request.y)
        return SuccessResponseModel(
            message=f"Operation '{operation}' calculated successfully",
            data=result
        )