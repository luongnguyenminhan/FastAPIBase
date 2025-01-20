"""
API V1 Endpoints

This file defines the API V1 endpoints for the application.
It includes endpoints for user management, item management, and math operations.

Dependencies:
- FastAPI for creating API endpoints
- Pydantic for data validation and serialization
- Various service classes for business logic

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict
from app.services.services.user_service import UserService
from app.services.services.item_service import ItemService
from app.services.services.math_service import MathService
from app.schemas.response_schema import UserResponse, ItemResponse, MessageResponse
from app.schemas.request_schema import UserRequest, ItemRequest, MathOperationRequest

api_router = APIRouter()  # Changed variable name to api_router

# User endpoints
@api_router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get(user_id)

@api_router.get("/users/email/{email}", response_model=UserResponse)
async def get_user_by_email(
    email: str,
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get_by_email(email)

@api_router.get("/users/{user_id}/items", response_model=List[ItemResponse])
async def get_user_items(
    user_id: int,
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get_user_items(user_id)

@api_router.get("/users/active", response_model=List[UserResponse])
async def get_active_users(
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get_active_users()

@api_router.post("/users/metrics", response_model=Dict[str, float])
async def calculate_user_metrics(
    metric_values: List[float],
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.calculate_user_metrics(metric_values)

@api_router.post("/users/", response_model=UserResponse)
async def create_user(
    user: UserRequest,
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.create(user)

@api_router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserRequest,
    user_service: UserService = Depends(UserService.get_self)
):
    user.id = user_id
    return await user_service.update(user)

@api_router.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(UserService.get_self)
):
    await user_service.delete(user_id)
    return {"message": f"User with id {user_id} has been deleted"}

# Item endpoints
@api_router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.get(item_id)

@api_router.post("/items/", response_model=ItemResponse)
async def create_item(
    item: ItemRequest,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.create(item)

@api_router.get("/items/category/{category}", response_model=List[ItemResponse])
async def get_items_by_category(
    category: str,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.get_by_category(category)

@api_router.put("/items/{item_id}/stock")
async def update_item_stock(
    item_id: int,
    quantity: int,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.update_stock(item_id, quantity)

@api_router.post("/items/calculate-value")
async def calculate_total_value(
    price: float,
    quantity: int,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.calculate_total_value(price, quantity)

@api_router.post("/items/calculate-discount")
async def calculate_discount(
    price: float,
    discount_percentage: float,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.calculate_discount(price, discount_percentage)

@api_router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item: ItemRequest,
    item_service: ItemService = Depends(ItemService.get_self)
):
    item.id = item_id
    return await item_service.update(item)

@api_router.delete("/items/{item_id}", response_model=MessageResponse)
async def delete_item(
    item_id: int,
    item_service: ItemService = Depends(ItemService.get_self)
):
    await item_service.delete(item_id)
    return {"message": f"Item with id {item_id} has been deleted"}

# Math operations endpoints
@api_router.post("/math/{operation}")
async def calculate(
    operation: str,
    request: MathOperationRequest,
    math_service: MathService = Depends(MathService.get_self)
):
    return await math_service.calculate_operation(operation, request.x, request.y)

__all__ = ["api_router"]  # Explicitly export api_router
