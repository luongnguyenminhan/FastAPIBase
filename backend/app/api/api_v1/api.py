from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.services.services.user_service import UserService
from app.services.services.item_service import ItemService
from app.services.services.math_service import MathService
from app.schemas.user import UserCreate, UserResponse
from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter()

# User endpoints
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get(user_id)

@router.get("/users/email/{email}", response_model=UserResponse)
async def get_user_by_email(
    email: str,
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get_by_email(email)

@router.get("/users/{user_id}/items", response_model=List[ItemResponse])
async def get_user_items(
    user_id: int,
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get_user_items(user_id)

# Item endpoints
@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.get(item_id)

@router.post("/items/", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.create(item)

@router.get("/items/category/{category}", response_model=List[ItemResponse])
async def get_items_by_category(
    category: str,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.get_by_category(category)

# Math operations endpoints
@router.get("/math/{operation}")
async def calculate(
    operation: str,
    x: float,
    y: float,
    math_service: MathService = Depends(MathService.get_self)
):
    return await math_service.calculate_operation(operation, x, y)
