"""
Math Controller (v2)

This file defines the MathController class for handling advanced math-related endpoints.
It follows the controller pattern to separate route definition from request handling logic.

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.1.0
"""

from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from app.services.services.math_service import MathService
from app.schemas.view_model.request import MathOperationViewModel
from app.schemas.common import BaseResponseModel, SuccessResponseModel


class MathController:
    """
    Controller handling advanced math-related endpoints including batch operations.
    """
    
    def __init__(self, router: APIRouter):
        self.router = router
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register all advanced math routes with the router."""
        self.router.add_api_route(
            "/batch",
            self.batch_calculate,
            methods=["POST"],
            response_model=BaseResponseModel[List[Dict[str, Any]]],
            summary="Batch calculate operations",
            description="Process multiple math operations in a single request",
            operation_id="batch_calculate_v2"
        )
    
    async def batch_calculate(
        self,
        operations: List[MathOperationViewModel],
        math_service: MathService = Depends(MathService.get_self)
    ) -> SuccessResponseModel:
        """
        Perform batch math operations.
        
        Args:
            operations: List of operations to perform
            math_service: The math service for business logic
            
        Returns:
            SuccessResponseModel: The results of all operations with metadata
        """
        results = []
        for op in operations:
            result = await math_service.calculate_operation(
                op.operation,
                op.x,
                op.y
            )
            results.append({
                "operation": op.operation,
                "result": result
            })
        
        return SuccessResponseModel(
            message="Batch operations calculated successfully",
            data=results,
            metadata={"operations_count": len(operations)}
        )