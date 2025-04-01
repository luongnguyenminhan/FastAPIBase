"""
Math Controller V2

This file defines the MathController class for handling math operation endpoints.
It follows the controller pattern to separate route definition from request handling logic.
This is the v2 version with enhanced features.

Author: Minh An
Last Modified: 23 Jun 2024
Version: 2.0.0
"""

from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
from app.services.services.math_service import MathService
from app.schemas.view_model.response import (
    OperationResultViewModel,
    EnhancedOperationResultViewModel
)
from app.schemas.business_model.response_base import BaseResponseModel, SuccessResponseModel


class MathController:
    """
    Controller handling math-related endpoints including various operations
    like add, subtract, multiply, etc. with enhanced features.
    """
    
    def __init__(self, router: APIRouter):
        self.router = router
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register all math routes with the router."""
        self.router.add_api_route(
            "/calculate/{operation}",
            self.calculate_operation,
            methods=["POST"],
            response_model=BaseResponseModel[EnhancedOperationResultViewModel],
            summary="Calculate operation",
            description="Perform a mathematical operation on two numbers with step-by-step details",
            operation_id="calculate_operation_v2"
        )
        
        self.router.add_api_route(
            "/operations",
            self.get_available_operations,
            methods=["GET"],
            response_model=BaseResponseModel[Dict[str, str]],
            summary="Available operations with descriptions",
            description="Get a list of available mathematical operations with descriptions",
            operation_id="get_available_operations_v2"
        )
        
        self.router.add_api_route(
            "/batch",
            self.calculate_multiple_operations,
            methods=["POST"],
            response_model=BaseResponseModel[Dict[str, Any]],
            summary="Batch calculate with summaries",
            description="Perform multiple mathematical operations in a single request with summary statistics",
            operation_id="calculate_multiple_operations_v2"
        )
        
        self.router.add_api_route(
            "/formula",
            self.calculate_formula,
            methods=["POST"],
            response_model=BaseResponseModel[float],
            summary="Calculate formula",
            description="Calculate result of a sequence of operations",
            operation_id="calculate_formula_v2"
        )
    
    async def calculate_operation(
        self,
        operation: str,
        x: float,
        y: float,
        round_to: Optional[int] = Query(None, ge=0, le=10),
        show_details: bool = Query(True),
        math_service: MathService = Depends(MathService.get_self)
    ) -> SuccessResponseModel:
        """
        Calculate a mathematical operation with enhanced details.
        
        Args:
            operation: The operation to perform (add, subtract, etc.)
            x: The first operand
            y: The second operand
            round_to: Number of decimal places to round to (optional)
            show_details: Whether to show step-by-step details
            math_service: The math service for business logic
            
        Returns:
            SuccessResponseModel: The calculation result with details
        """
        result = await math_service.calculate_operation(operation, x, y)
        
        # Round result if specified
        if round_to is not None:
            result = round(result, round_to)
        
        # Create step-by-step explanation based on operation
        steps = []
        if show_details:
            if operation == "add":
                steps = [f"Add {x} and {y}", f"Result: {result}"]
            elif operation == "subtract":
                steps = [f"Subtract {y} from {x}", f"Result: {result}"]
            elif operation == "multiply":
                steps = [f"Multiply {x} by {y}", f"Result: {result}"]
            elif operation == "divide":
                steps = [f"Divide {x} by {y}", f"Result: {result}"]
            elif operation == "power":
                steps = [f"Raise {x} to the power of {y}", f"Result: {result}"]
        
        # Create enhanced response
        enhanced_result = EnhancedOperationResultViewModel(
            operation=operation,
            x=x,
            y=y,
            result=result,
            steps=steps if show_details else None
        )
        
        return SuccessResponseModel(
            message=f"Operation '{operation}' calculated successfully",
            data=enhanced_result,
            metadata={
                "rounded": round_to is not None,
                "decimal_places": round_to,
                "show_details": show_details
            }
        )
    
    async def get_available_operations(
        self,
        with_examples: bool = Query(True),
        math_service: MathService = Depends(MathService.get_self)
    ) -> SuccessResponseModel:
        """
        Get a list of available mathematical operations with descriptions.
        
        Args:
            with_examples: Whether to include example usage
            math_service: The math service for business logic
            
        Returns:
            SuccessResponseModel: The list of available operations with descriptions
        """
        operations = await math_service.get_available_operations()
        
        # Create descriptions for each operation
        operation_info = {}
        
        for op in operations:
            if op == "add":
                description = "Addition operation: adds two numbers together"
                example = "5 + 3 = 8" if with_examples else None
            elif op == "subtract":
                description = "Subtraction operation: subtracts the second number from the first"
                example = "5 - 3 = 2" if with_examples else None
            elif op == "multiply":
                description = "Multiplication operation: multiplies two numbers together"
                example = "5 * 3 = 15" if with_examples else None
            elif op == "divide":
                description = "Division operation: divides the first number by the second"
                example = "6 / 3 = 2" if with_examples else None
            elif op == "power":
                description = "Power operation: raises the first number to the power of the second"
                example = "2 ^ 3 = 8" if with_examples else None
            else:
                description = f"Unknown operation: {op}"
                example = None
            
            operation_info[op] = {
                "description": description,
                "example": example
            }
        
        return SuccessResponseModel(
            message="Available operations retrieved successfully",
            data=operation_info,
            metadata={
                "with_examples": with_examples,
                "count": len(operations)
            }
        )
    
    async def calculate_multiple_operations(
        self,
        operations: List[Dict[str, Any]],
        include_individual_results: bool = Query(True),
        math_service: MathService = Depends(MathService.get_self)
    ) -> SuccessResponseModel:
        """
        Calculate multiple operations in a batch with summary statistics.
        
        Args:
            operations: List of operations with operation name and operands
            include_individual_results: Whether to include individual operation results
            math_service: The math service for business logic
            
        Returns:
            SuccessResponseModel: The results with summary statistics
        """
        results = await math_service.calculate_multiple_operations(operations)
        
        # Create a list of result view models if requested
        individual_results = None
        if include_individual_results:
            individual_results = []
            for i, op_data in enumerate(operations):
                individual_results.append(
                    OperationResultViewModel(
                        operation=op_data.get('operation', ''),
                        x=op_data.get('x', 0.0),
                        y=op_data.get('y', 0.0),
                        result=results[i]
                    )
                )
        
        # Calculate summary statistics
        summary = {
            "count": len(results),
            "sum": sum(results),
            "average": sum(results) / len(results) if results else 0,
            "min": min(results) if results else None,
            "max": max(results) if results else None
        }
            
        return SuccessResponseModel(
            message=f"Successfully calculated {len(results)} operations",
            data={
                "summary": summary,
                "results": individual_results
            },
            metadata={
                "operations_count": len(operations),
                "include_individual_results": include_individual_results
            }
        )
    
    async def calculate_formula(
        self,
        formula: List[Dict[str, Any]],
        math_service: MathService = Depends(MathService.get_self)
    ) -> SuccessResponseModel:
        """
        Calculate a sequence of operations in order (formula).
        
        Args:
            formula: List of operations to execute in sequence
            math_service: The math service for business logic
            
        Returns:
            SuccessResponseModel: The final result with execution trace
        """
        # Process operations in sequence
        result = 0
        execution_trace = []
        
        try:
            # Execute first operation to get initial result
            if len(formula) > 0:
                first_op = formula[0]
                result = await math_service.calculate_operation(
                    first_op.get('operation', 'add'),
                    first_op.get('x', 0.0),
                    first_op.get('y', 0.0)
                )
                execution_trace.append({
                    "step": 1,
                    "operation": first_op.get('operation', 'add'),
                    "x": first_op.get('x', 0.0),
                    "y": first_op.get('y', 0.0),
                    "result": result
                })
            
            # Execute remaining operations using result of previous step
            for i, op_data in enumerate(formula[1:], start=2):
                operation = op_data.get('operation', 'add')
                y = op_data.get('y', 0.0)
                
                # Use result of previous step as x
                result = await math_service.calculate_operation(operation, result, y)
                
                execution_trace.append({
                    "step": i,
                    "operation": operation,
                    "x": execution_trace[-1]["result"],  # Previous result
                    "y": y,
                    "result": result
                })
                
            return SuccessResponseModel(
                message="Formula calculated successfully",
                data=result,
                metadata={
                    "steps_count": len(formula),
                    "execution_trace": execution_trace
                }
            )
        except Exception as e:
            # Error is handled by middleware, just provide additional context
            return SuccessResponseModel(
                message="Error calculating formula",
                data=None,
                metadata={
                    "error": str(e),
                    "execution_trace": execution_trace
                }
            )