"""
User Controller V2

This file defines the UserController class for handling user-related endpoints.
It follows the controller pattern to separate route definition from request handling logic.
This is the v2 version with enhanced features.

Author: Minh An
Last Modified: 23 Jun 2024
Version: 2.0.0
"""

from typing import List, Dict, Optional

from app.db.base import get_db
from app.schemas.business_model.response_base import BaseResponseModel, SuccessResponseModel
from app.schemas.view_model.request import UserRequestViewModel
from app.schemas.view_model.response import (
    ItemResponseViewModel,
    UserResponseViewModel,
    MessageResponseViewModel,
    EnhancedUserResponseViewModel
)
from app.services.services.user_service import UserService
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session


class UserController:
    """
    Controller handling user-related endpoints including user retrieval,
    creation, updating, and deletion with enhanced features.
    """

    def __init__(self, router: APIRouter, db: Session = Depends(get_db)):
        """
        Initialize the controller with router and database session.
        
        Args:
            router: FastAPI router instance
            db: Database session
        """
        self.router = router
        self.user_service = UserService.get_self(db)
        self._register_routes()

    def _register_routes(self) -> None:
        """Register all user routes with the router."""
        self.router.add_api_route(
            "/{user_id}",
            self.get_user,
            methods=["GET"],
            response_model=BaseResponseModel[EnhancedUserResponseViewModel],
            summary="Get user by ID",
            description="Retrieve user details by user ID with additional information",
            operation_id="get_user_v2"
        )

        self.router.add_api_route(
            "/email/{email}",
            self.get_user_by_email,
            methods=["GET"],
            response_model=BaseResponseModel[EnhancedUserResponseViewModel],
            summary="Get user by email",
            description="Retrieve user details by email address with additional information",
            operation_id="get_user_by_email_v2"
        )

        # Enhanced with pagination
        self.router.add_api_route(
            "/{user_id}/items",
            self.get_user_items,
            methods=["GET"],
            response_model=BaseResponseModel[List[ItemResponseViewModel]],
            summary="Get user items",
            description="Retrieve all items owned by a user with pagination",
            operation_id="get_user_items_v2"
        )

        # Enhanced with filtering
        self.router.add_api_route(
            "/active",
            self.get_active_users,
            methods=["GET"],
            response_model=BaseResponseModel[List[UserResponseViewModel]],
            summary="Get active users",
            description="Retrieve active users with filtering options",
            operation_id="get_active_users_v2"
        )

        # Enhanced with more detailed response
        self.router.add_api_route(
            "/metrics",
            self.calculate_user_metrics,
            methods=["POST"],
            response_model=BaseResponseModel[Dict[str, float]],
            summary="Calculate user metrics",
            description="Calculate metrics based on provided values with detailed breakdown",
            operation_id="calculate_user_metrics_v2"
        )

        self.router.add_api_route(
            "/",
            self.create_user,
            methods=["POST"],
            response_model=BaseResponseModel[EnhancedUserResponseViewModel],
            summary="Create user",
            description="Create a new user with enhanced response",
            operation_id="create_user_v2"
        )

        self.router.add_api_route(
            "/{user_id}",
            self.update_user,
            methods=["PUT"],
            response_model=BaseResponseModel[EnhancedUserResponseViewModel],
            summary="Update user",
            description="Update an existing user with enhanced response",
            operation_id="update_user_v2"
        )

        self.router.add_api_route(
            "/{user_id}",
            self.delete_user,
            methods=["DELETE"],
            response_model=BaseResponseModel[MessageResponseViewModel],
            summary="Delete user",
            description="Delete a user by ID",
            operation_id="delete_user_v2"
        )

    async def get_user(
            self,
            user_id: int,
            include_items: bool = Query(False)
    ) -> SuccessResponseModel:
        """
        Get a user by ID with enhanced options.
        
        Args:
            user_id: The ID of the user to retrieve
            include_items: Whether to include the user's items
            
        Returns:
            SuccessResponseModel: The retrieved user with additional information
        """
        user = await self.user_service.get(user_id)

        # Include items if requested
        items = None
        if include_items:
            items = await self.user_service.get_user_items(user_id)

        # Create enhanced response with additional information
        enhanced_user = EnhancedUserResponseViewModel(
            **user.dict(),
            item_count=len(items) if items else 0,
            items=items if items else None
        )

        return SuccessResponseModel(
            message="User retrieved successfully",
            data=enhanced_user,
            metadata={
                "include_items": include_items,
                "has_items": items is not None and len(items) > 0
            }
        )

    async def get_user_by_email(
            self,
            email: str,
            include_items: bool = Query(False)
    ) -> SuccessResponseModel:
        """
        Get a user by email with enhanced options.
        
        Args:
            email: The email of the user to retrieve
            include_items: Whether to include the user's items
            
        Returns:
            SuccessResponseModel: The retrieved user with additional information
        """
        user = await self.user_service.get_by_email(email)

        # Include items if requested
        items = None
        if include_items and user:
            items = await self.user_service.get_user_items(user.id)

        # Create enhanced response with additional information
        enhanced_user = EnhancedUserResponseViewModel(
            **user.dict(),
            item_count=len(items) if items else 0,
            items=items if items else None
        )

        return SuccessResponseModel(
            message="User retrieved successfully",
            data=enhanced_user,
            metadata={
                "include_items": include_items,
                "has_items": items is not None and len(items) > 0
            }
        )

    async def get_user_items(
            self,
            user_id: int,
            skip: int = Query(0, ge=0),
            limit: int = Query(10, ge=1, le=100),
            category: Optional[str] = None
    ) -> SuccessResponseModel:
        """
        Get items owned by a user with pagination and filtering.
        
        Args:
            user_id: The ID of the user
            skip: The number of items to skip
            limit: The maximum number of items to return
            category: Optional category filter
            
        Returns:
            SuccessResponseModel: The user's items with pagination metadata
        """
        items = await self.user_service.get_user_items(user_id)

        # Filter by category if provided
        if category:
            items = [item for item in items if item.category == category]

        # Apply pagination (in a real app, this would be done at the database level)
        paginated_items = items[skip:skip + limit]

        return SuccessResponseModel(
            message="User items retrieved successfully",
            data=paginated_items,
            metadata={
                "total": len(items),
                "page": skip // limit + 1,
                "page_size": limit,
                "pages": (len(items) + limit - 1) // limit,
                "filtered_by_category": category is not None
            }
        )

    async def get_active_users(
            self,
            role: Optional[str] = None,
            search: Optional[str] = None
    ) -> SuccessResponseModel:
        """
        Get active users with filtering options.
        
        Args:
            role: Optional role filter
            search: Optional search term for name or email
            
        Returns:
            SuccessResponseModel: The active users with filtering metadata
        """
        users = await self.user_service.get_active_users()

        # Apply role filter if provided
        if role:
            users = [user for user in users if user.role == role]

        # Apply search filter if provided
        if search:
            search = search.lower()
            users = [
                user for user in users
                if search in user.email.lower() or
                   search in user.full_name.lower()
            ]

        return SuccessResponseModel(
            message="Active users retrieved successfully",
            data=users,
            metadata={
                "total": len(users),
                "filtered_by_role": role is not None,
                "filtered_by_search": search is not None
            }
        )

    async def calculate_user_metrics(
            self,
            metric_values: List[float]
    ) -> SuccessResponseModel:
        """
        Calculate user metrics with detailed breakdown.
        
        Args:
            metric_values: List of metric values to calculate
            
        Returns:
            SuccessResponseModel: The calculated metrics with detailed breakdown
        """
        metrics = await self.user_service.calculate_user_metrics(metric_values)

        # Add more detailed statistics
        additional_metrics = {
            "min": min(metric_values) if metric_values else 0,
            "max": max(metric_values) if metric_values else 0,
            "count": len(metric_values)
        }

        # Combine all metrics
        all_metrics = {**metrics, **additional_metrics}

        return SuccessResponseModel(
            message="User metrics calculated successfully",
            data=all_metrics,
            metadata={
                "raw_values": metric_values
            }
        )

    async def create_user(
            self,
            user: UserRequestViewModel
    ) -> SuccessResponseModel:
        """
        Create a new user with enhanced response.
        
        Args:
            user: The user data
            
        Returns:
            SuccessResponseModel: The created user with additional information
        """
        created_user = await self.user_service.create(user)

        # Create enhanced response
        enhanced_user = EnhancedUserResponseViewModel(
            **created_user.dict(),
            item_count=0,
            items=None
        )

        return SuccessResponseModel(
            message="User created successfully",
            data=enhanced_user,
            metadata={
                "created_at": enhanced_user.created_at
            }
        )

    async def update_user(
            self,
            user_id: int,
            user: UserRequestViewModel
    ) -> SuccessResponseModel:
        """
        Update an existing user with enhanced response.
        
        Args:
            user_id: The ID of the user to update
            user: The updated user data
            
        Returns:
            SuccessResponseModel: The updated user with additional information
        """
        # Get the original user first for comparison
        original_user = await self.user_service.get(user_id)

        # Update the user
        user.id = user_id
        updated_user = await self.user_service.update(user)

        # Get the user's items
        items = await self.user_service.get_user_items(user_id)

        # Create enhanced response
        enhanced_user = EnhancedUserResponseViewModel(
            **updated_user.dict(),
            item_count=len(items),
            items=None  # Don't include full items in update response
        )

        # Determine what fields were updated
        updated_fields = []
        for field in updated_user.dict():
            if getattr(original_user, field) != getattr(updated_user, field):
                updated_fields.append(field)

        return SuccessResponseModel(
            message="User updated successfully",
            data=enhanced_user,
            metadata={
                "updated_at": enhanced_user.updated_at,
                "updated_fields": updated_fields
            }
        )

    async def delete_user(
            self,
            user_id: int
    ) -> SuccessResponseModel:
        """
        Delete a user.
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            SuccessResponseModel: Confirmation message
        """
        # Get the user before deletion for metadata
        user = await self.user_service.get(user_id)

        # Delete the user
        await self.user_service.delete(user_id)

        return SuccessResponseModel(
            message=f"User with id {user_id} has been deleted",
            data={"message": f"User with id {user_id} has been deleted"},
            metadata={
                "deleted_user_email": user.email,
                "deleted_at": user.updated_at
            }
        )
