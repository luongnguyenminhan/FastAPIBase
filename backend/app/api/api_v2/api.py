"""
API V2 Endpoints

This file defines the API V2 endpoints for the application.
It includes advanced endpoints for user management, item management, and math operations.

Dependencies:
- FastAPI for creating API endpoints
- Pydantic for data validation and serialization
- Various service classes for business logic

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from fastapi import APIRouter, Depends, Query
from typing import List
from app.services.services.user_service import UserService
from app.services.services.item_service import ItemService
from app.services.services.math_service import MathService
from app.schemas.response_schema import (
    UserResponse, ItemResponse, UserMetricsResponse,
    ItemValueResponse, ItemDiscountResponse
)
from app.schemas.request_schema import (
    UserMetricsRequest, ItemStockUpdateRequest,
    ItemDiscountRequest, MathOperationRequest
)

api_router = APIRouter()  # Changed variable name to api_router


# Advanced User endpoints
@api_router.get("/users/active", response_model=List[UserResponse])
async def get_active_users(
        user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get_active_users()


@api_router.post("/users/metrics", response_model=UserMetricsResponse)
async def calculate_user_metrics(
        request: UserMetricsRequest,
        user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.calculate_user_metrics(request.metric_values)


# Advanced Item endpoints
@api_router.patch("/items/{item_id}/stock", response_model=ItemResponse)
async def update_item_stock(
        item_id: int,
        request: ItemStockUpdateRequest,
        item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.update_stock(item_id, request.quantity)


@api_router.get("/items/{item_id}/value", response_model=ItemValueResponse)
async def calculate_item_value(
        item_id: int,
        quantity: int,
        item_service: ItemService = Depends(ItemService.get_self)
):
    item = await item_service.get(item_id)
    return await item_service.calculate_total_value(item.price, quantity)


@api_router.get("/items/{item_id}/discount", response_model=ItemDiscountResponse)
async def calculate_item_discount(
        item_id: int,
        discount_percentage: float = Query(..., gt=0, lt=100),
        item_service: ItemService = Depends(ItemService.get_self)
):
    item = await item_service.get(item_id)
    return await item_service.calculate_discount(item.price, discount_percentage)


# Advanced Math operations
@api_router.post("/math/batch")
async def batch_calculate(
        operations: List[MathOperationRequest],
        math_service: MathService = Depends(MathService.get_self)
):
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
    return results


__all__ = ["api_router"]  # Explicitly export api_router
