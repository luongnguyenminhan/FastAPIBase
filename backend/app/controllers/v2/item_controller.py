"""
Item Controller (v2)

This file defines the ItemController class for handling advanced item-related endpoints.
It follows the controller pattern to separate route definition from request handling logic.

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.1.0
"""

from fastapi import APIRouter, Depends, Query
from app.services.services.item_service import ItemService
from app.schemas.view_model.response import (
    ItemResponseViewModel,
    ItemValueResponseViewModel,
    ItemDiscountResponseViewModel
)
from app.schemas.view_model.request import ItemStockUpdateViewModel
from app.schemas.common import BaseResponseModel, SuccessResponseModel


class ItemController:
    """
    Controller handling advanced item-related endpoints including 
    stock updates, value calculations, and discounts.
    """
    
    def __init__(self, router: APIRouter):
        self.router = router
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register all advanced item routes with the router."""
        self.router.add_api_route(
            "/{item_id}/stock",
            self.update_item_stock,
            methods=["PATCH"],
            response_model=BaseResponseModel[ItemResponseViewModel],
            summary="Update item stock",
            description="Update item stock quantity with partial update",
            operation_id="update_item_stock_v2"
        )
        
        self.router.add_api_route(
            "/{item_id}/value",
            self.calculate_item_value,
            methods=["GET"],
            response_model=BaseResponseModel[ItemValueResponseViewModel],
            summary="Calculate item value",
            description="Calculate total value for a specific item",
            operation_id="calculate_item_value_v2"
        )
        
        self.router.add_api_route(
            "/{item_id}/discount",
            self.calculate_item_discount,
            methods=["GET"],
            response_model=BaseResponseModel[ItemDiscountResponseViewModel],
            summary="Calculate item discount",
            description="Calculate discounted price for a specific item",
            operation_id="calculate_item_discount_v2"
        )
    
    async def update_item_stock(
        self,
        item_id: int,
        request: ItemStockUpdateViewModel,
        item_service: ItemService = Depends(ItemService.get_self)
    ) -> SuccessResponseModel:
        """
        Update item stock using PATCH method.
        
        Args:
            item_id: The ID of the item to update
            request: The update data containing quantity
            item_service: The item service for business logic
            
        Returns:
            SuccessResponseModel: The updated item with metadata
        """
        updated_item = await item_service.update_stock(item_id, request.quantity)
        return SuccessResponseModel(
            message="Item stock updated successfully",
            data=updated_item,
            metadata={"previous_version": "Not tracked in this version"}
        )
    
    async def calculate_item_value(
        self,
        item_id: int,
        quantity: int,
        item_service: ItemService = Depends(ItemService.get_self)
    ) -> SuccessResponseModel:
        """
        Calculate value for a specific item.
        
        Args:
            item_id: The ID of the item
            quantity: The quantity of items
            item_service: The item service for business logic
            
        Returns:
            SuccessResponseModel: The calculation result with metadata
        """
        item = await item_service.get(item_id)
        total_value = await item_service.calculate_total_value(item.price, quantity)
        result = ItemValueResponseViewModel(
            item_id=item_id,
            quantity=quantity,
            total_value=total_value
        )
        return SuccessResponseModel(
            message="Item value calculated successfully",
            data=result,
            metadata={"item_name": item.title, "unit_price": float(item.price)}
        )
    
    async def calculate_item_discount(
        self,
        item_id: int,
        discount_percentage: float = Query(..., gt=0, lt=100),
        item_service: ItemService = Depends(ItemService.get_self)
    ) -> SuccessResponseModel:
        """
        Calculate discount for a specific item.
        
        Args:
            item_id: The ID of the item
            discount_percentage: The discount percentage (0-100)
            item_service: The item service for business logic
            
        Returns:
            SuccessResponseModel: The calculation result with metadata
        """
        item = await item_service.get(item_id)
        final_price = await item_service.calculate_discount(item.price, discount_percentage)
        result = ItemDiscountResponseViewModel(
            item_id=item_id,
            original_price=item.price,
            discount_percentage=discount_percentage,
            final_price=final_price
        )
        return SuccessResponseModel(
            message="Item discount calculated successfully",
            data=result,
            metadata={"item_name": item.title, "savings": float(item.price) - float(final_price)}
        )