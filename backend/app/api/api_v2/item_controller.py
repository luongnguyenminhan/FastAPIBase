from fastapi import APIRouter, Depends, Query
from app.services.services.item_service import ItemService
from app.schemas.response_schema import ItemResponse, ItemValueResponse, ItemDiscountResponse
from app.schemas.request_schema import ItemStockUpdateRequest

item_router = APIRouter()


# Advanced Item endpoints
@item_router.patch("/{item_id}/stock", response_model=ItemResponse, operation_id="update_item_stock_v2")
async def update_item_stock(
        item_id: int,
        request: ItemStockUpdateRequest,
        item_service: ItemService = Depends(ItemService.get_self)
):
    return await item_service.update_stock(item_id, request.quantity)


@item_router.get("/{item_id}/value", response_model=ItemValueResponse, operation_id="calculate_item_value_v2")
async def calculate_item_value(
        item_id: int,
        quantity: int,
        item_service: ItemService = Depends(ItemService.get_self)
):
    item = await item_service.get(item_id)
    return await item_service.calculate_total_value(item.price, quantity)


@item_router.get("/{item_id}/discount", response_model=ItemDiscountResponse, operation_id="calculate_item_discount_v2")
async def calculate_item_discount(
        item_id: int,
        discount_percentage: float = Query(..., gt=0, lt=100),
        item_service: ItemService = Depends(ItemService.get_self)
):
    item = await item_service.get(item_id)
    return await item_service.calculate_discount(item.price, discount_percentage)
