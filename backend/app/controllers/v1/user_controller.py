"""
User Controller

This file defines the UserController class for handling user-related endpoints.
It follows the controller pattern to separate route definition from request handling logic.

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.1.0
"""

from fastapi import APIRouter, Depends
from typing import List, Dict
from app.services.services.user_service import UserService
from app.schemas.view_model.response import (
    ItemResponseViewModel,
    UserResponseViewModel,
    MessageResponseViewModel
)
from app.schemas.view_model.request import UserRequestViewModel
from app.schemas.common import BaseResponseModel, SuccessResponseModel


class UserController:
    """
    Controller handling user-related endpoints including user retrieval,
    creation, updating, and deletion.
    """
    
    def __init__(self, router: APIRouter):
        self.router = router
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register all user routes with the router."""
        self.router.add_api_route(
            "/{user_id}",
            self.get_user,
            methods=["GET"],
            response_model=BaseResponseModel[UserResponseViewModel],
            summary="Get user by ID",
            description="Retrieve user details by user ID",
            operation_id="get_user_v1"
        )
        
        self.router.add_api_route(
            "/email/{email}",
            self.get_user_by_email,
            methods=["GET"],
            response_model=BaseResponseModel[UserResponseViewModel],
            summary="Get user by email",
            description="Retrieve user details by email address",
            operation_id="get_user_by_email_v1"
        )
        
        self.router.add_api_route(
            "/{user_id}/items",
            self.get_user_items,
            methods=["GET"],
            response_model=BaseResponseModel[List[ItemResponseViewModel]],
            summary="Get user items",
            description="Retrieve all items owned by a user",
            operation_id="get_user_items_v1"
        )
        
        self.router.add_api_route(
            "/active",
            self.get_active_users,
            methods=["GET"],
            response_model=BaseResponseModel[List[UserResponseViewModel]],
            summary="Get active users",
            description="Retrieve all active users",
            operation_id="get_active_users_v1"
        )
        
        self.router.add_api_route(
            "/metrics",
            self.calculate_user_metrics,
            methods=["POST"],
            response_model=BaseResponseModel[Dict[str, float]],
            summary="Calculate user metrics",
            description="Calculate metrics based on provided values",
            operation_id="calculate_user_metrics_v1"
        )
        
        self.router.add_api_route(
            "/",
            self.create_user,
            methods=["POST"],
            response_model=BaseResponseModel[UserResponseViewModel],
            summary="Create user",
            description="Create a new user",
            operation_id="create_user_v1"
        )
        
        self.router.add_api_route(
            "/{user_id}",
            self.update_user,
            methods=["PUT"],
            response_model=BaseResponseModel[UserResponseViewModel],
            summary="Update user",
            description="Update an existing user",
            operation_id="update_user_v1"
        )
        
        self.router.add_api_route(
            "/{user_id}",
            self.delete_user,
            methods=["DELETE"],
            response_model=BaseResponseModel[MessageResponseViewModel],
            summary="Delete user",
            description="Delete a user by ID",
            operation_id="delete_user_v1"
        )
    
    async def get_user(
        self,
        user_id: int,
        user_service: UserService = Depends(UserService.get_self)
    ) -> SuccessResponseModel:
        """
        Get a user by ID.
        
        Args:
            user_id: The ID of the user to retrieve
            user_service: The user service for business logic
            
        Returns:
            SuccessResponseModel: The retrieved user
        """
        user = await user_service.get(user_id)
        return SuccessResponseModel(
            message="User retrieved successfully",
            data=user
        )
    
    async def get_user_by_email(
        self,
        email: str,
        user_service: UserService = Depends(UserService.get_self)
    ) -> SuccessResponseModel:
        """
        Get a user by email.
        
        Args:
            email: The email of the user to retrieve
            user_service: The user service for business logic
            
        Returns:
            SuccessResponseModel: The retrieved user
        """
        user = await user_service.get_by_email(email)
        return SuccessResponseModel(
            message="User retrieved successfully",
            data=user
        )
    
    async def get_user_items(
        self,
        user_id: int,
        user_service: UserService = Depends(UserService.get_self)
    ) -> SuccessResponseModel:
        """
        Get items owned by a user.
        
        Args:
            user_id: The ID of the user
            user_service: The user service for business logic
            
        Returns:
            SuccessResponseModel: The user's items
        """
        items = await user_service.get_user_items(user_id)
        return SuccessResponseModel(
            message="User items retrieved successfully",
            data=items
        )
    
    async def get_active_users(
        self,
        user_service: UserService = Depends(UserService.get_self)
    ) -> SuccessResponseModel:
        """
        Get all active users.
        
        Args:
            user_service: The user service for business logic
            
        Returns:
            SuccessResponseModel: The active users
        """
        users = await user_service.get_active_users()
        return SuccessResponseModel(
            message="Active users retrieved successfully",
            data=users
        )
    
    async def calculate_user_metrics(
        self,
        metric_values: List[float],
        user_service: UserService = Depends(UserService.get_self)
    ) -> SuccessResponseModel:
        """
        Calculate user metrics.
        
        Args:
            metric_values: List of metric values to calculate
            user_service: The user service for business logic
            
        Returns:
            SuccessResponseModel: The calculated metrics
        """
        metrics = await user_service.calculate_user_metrics(metric_values)
        return SuccessResponseModel(
            message="User metrics calculated successfully",
            data=metrics
        )
    
    async def create_user(
        self,
        user: UserRequestViewModel,
        user_service: UserService = Depends(UserService.get_self)
    ) -> SuccessResponseModel:
        """
        Create a new user.
        
        Args:
            user: The user data
            user_service: The user service for business logic
            
        Returns:
            SuccessResponseModel: The created user
        """
        created_user = await user_service.create(user)
        return SuccessResponseModel(
            message="User created successfully",
            data=created_user
        )
    
    async def update_user(
        self,
        user_id: int,
        user: UserRequestViewModel,
        user_service: UserService = Depends(UserService.get_self)
    ) -> SuccessResponseModel:
        """
        Update an existing user.
        
        Args:
            user_id: The ID of the user to update
            user: The updated user data
            user_service: The user service for business logic
            
        Returns:
            SuccessResponseModel: The updated user
        """
        user.id = user_id
        updated_user = await user_service.update(user)
        return SuccessResponseModel(
            message="User updated successfully",
            data=updated_user
        )
    
    async def delete_user(
        self,
        user_id: int,
        user_service: UserService = Depends(UserService.get_self)
    ) -> SuccessResponseModel:
        """
        Delete a user.
        
        Args:
            user_id: The ID of the user to delete
            user_service: The user service for business logic
            
        Returns:
            SuccessResponseModel: Confirmation message
        """
        await user_service.delete(user_id)
        return SuccessResponseModel(
            message=f"User with id {user_id} has been deleted",
            data={"message": f"User with id {user_id} has been deleted"}
        )