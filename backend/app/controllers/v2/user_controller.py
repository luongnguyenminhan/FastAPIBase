"""
User Controller (v2)

This file defines the UserController class for handling advanced user-related endpoints.
It follows the controller pattern to separate route definition from request handling logic.

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.1.0
"""

from fastapi import APIRouter, Depends
from typing import List
from app.services.services.user_service import UserService
from app.schemas.view_model.response import (
    UserResponseViewModel,
    UserMetricsResponseViewModel
)
from app.schemas.view_model.request import UserMetricsViewModel
from app.schemas.common import BaseResponseModel, SuccessResponseModel


class UserController:
    """
    Controller handling advanced user-related endpoints including user metrics and filtering.
    """
    
    def __init__(self, router: APIRouter):
        self.router = router
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register all advanced user routes with the router."""
        self.router.add_api_route(
            "/active",
            self.get_active_users,
            methods=["GET"],
            response_model=BaseResponseModel[List[UserResponseViewModel]],
            summary="Get active users",
            description="Retrieve all active users with additional metadata",
            operation_id="get_active_users_v2"
        )
        
        self.router.add_api_route(
            "/metrics",
            self.calculate_user_metrics,
            methods=["POST"],
            response_model=BaseResponseModel[UserMetricsResponseViewModel],
            summary="Calculate user metrics",
            description="Calculate advanced metrics based on provided values",
            operation_id="calculate_user_metrics_v2"
        )
    
    async def get_active_users(
        self,
        user_service: UserService = Depends(UserService.get_self)
    ) -> SuccessResponseModel:
        """
        Get all active users with additional metadata.
        
        Args:
            user_service: The user service for business logic
            
        Returns:
            SuccessResponseModel: The active users with metadata
        """
        users = await user_service.get_active_users()
        return SuccessResponseModel(
            message="Active users retrieved successfully",
            data=users,
            metadata={"total_count": len(users)}
        )
    
    async def calculate_user_metrics(
        self,
        request: UserMetricsViewModel,
        user_service: UserService = Depends(UserService.get_self)
    ) -> SuccessResponseModel:
        """
        Calculate user metrics with additional metadata.
        
        Args:
            request: The request containing metric values
            user_service: The user service for business logic
            
        Returns:
            SuccessResponseModel: The calculated metrics with metadata
        """
        metrics = await user_service.calculate_user_metrics(request.metric_values)
        return SuccessResponseModel(
            message="User metrics calculated successfully",
            data=metrics,
            metadata={"metrics_count": len(request.metric_values)}
        )