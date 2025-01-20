from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.services.services.user_service import UserService
from app.services.services.item_service import ItemService
from app.services.services.math_service import MathService
from app.schemas.user import UserCreate, UserResponse, UserMetrics
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter()

# Advanced User endpoints
@router.get("/users/active", response_model=List[UserResponse])
async def get_active_users(
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get_active_users()

@router.post("/users/metrics")
async def calculate_user_metrics(
    values: List[float],
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.calculate_user_metrics(values)

# Advanced Item endpoints
@router.patch("/items/{item_id}/stock")
async def update_item_stock(
    item_id: int,
    quantity: int,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.update_stock(item_id, quantity)

@router.get("/items/{item_id}/value")
async def calculate_item_value(
    item_id: int,
    quantity: int,
    item_service: ItemService = Depends(ItemService.get_self)
):
    item = await item_service.get(item_id)
    return await item_service.calculate_total_value(item.price, quantity)

@router.get("/items/{item_id}/discount")
async def calculate_item_discount(
    item_id: int,
    discount_percentage: float = Query(..., gt=0, lt=100),
    item_service: ItemService = Depends(ItemService.get_self)
):
    item = await item_service.get(item_id)
    return await item_service.calculate_discount(item.price, discount_percentage)

# Advanced Math operations
@router.post("/math/batch")
async def batch_calculate(
    operations: List[dict],
    math_service: MathService = Depends(MathService.get_self)
):
    results = []
    for op in operations:
        result = await math_service.calculate_operation(
            op["operation"],
            op["x"],
            op["y"]
        )
        results.append({
            "operation": op["operation"],
            "result": result
        })
    return results
