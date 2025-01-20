from fastapi import APIRouter, Depends
from typing import List
from app.services.services.item_service import ItemService
from app.schemas.response_schema import ItemResponse, MessageResponse
from app.schemas.request_schema import ItemRequest

item_router = APIRouter()

# Item endpoints
@item_router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.get(item_id)

@item_router.post("/", response_model=ItemResponse)
async def create_item(
    item: ItemRequest,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.create(item)

@item_router.get("/category/{category}", response_model=List[ItemResponse])
async def get_items_by_category(
    category: str,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.get_by_category(category)

@item_router.put("/{item_id}/stock")
async def update_item_stock(
    item_id: int,
    quantity: int,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.update_stock(item_id, quantity)

@item_router.post("/calculate-value")
async def calculate_total_value(
    price: float,
    quantity: int,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.calculate_total_value(price, quantity)

@item_router.post("/calculate-discount")
async def calculate_discount(
    price: float,
    discount_percentage: float,
    item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.calculate_discount(price, discount_percentage)

@item_router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item: ItemRequest,
    item_service: ItemService = Depends(ItemService.get_self)
):
    item.id = item_id
    return await item_service.update(item)

@item_router.delete("/{item_id}", response_model=MessageResponse)
async def delete_item(
    item_id: int,
    item_service: ItemService = Depends(ItemService.get_self)
):
    await item_service.delete(item_id)
    return {"message": f"Item with id {item_id} has been deleted"}
