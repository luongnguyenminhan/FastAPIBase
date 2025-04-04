"""
Item Controller

This file defines the ItemController class for handling item-related endpoints.
It follows the controller pattern to separate route definition from request handling logic.

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.1.0
"""

from typing import List

from app.db.base import get_db
from app.schemas.business_model.response_base import BaseResponseModel, SuccessResponseModel
from app.schemas.view_model.request import (
    ItemRequestViewModel,
    ItemStockUpdateViewModel
)
from app.schemas.view_model.response import (
    ItemResponseViewModel,
    MessageResponseViewModel,
    ItemValueResponseViewModel,
    ItemDiscountResponseViewModel
)
from app.services.services.item_service import ItemService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


class ItemController:
    """
    Controller handling item-related endpoints including item retrieval,
    creation, updating, deletion, and calculations.
    """

    def __init__(self, router: APIRouter, db: Session = Depends(get_db)):
        """
        Initialize the controller with router and database session.
        
        Args:
            router: FastAPI router instance
            db: Database session
        """
        self.router = router
        self.item_service = ItemService.get_self(db)
        self._register_routes()

    def _register_routes(self) -> None:
        """Register all item routes with the router."""
        self.router.add_api_route(
            "/{item_id}",
            self.get_item,
            methods=["GET"],
            response_model=BaseResponseModel[ItemResponseViewModel],
            summary="Get item by ID",
            description="Retrieve item details by item ID",
            operation_id="get_item_v1"
        )

        self.router.add_api_route(
            "/",
            self.create_item,
            methods=["POST"],
            response_model=BaseResponseModel[ItemResponseViewModel],
            summary="Create item",
            description="Create a new item",
            operation_id="create_item_v1"
        )

        self.router.add_api_route(
            "/category/{category}",
            self.get_items_by_category,
            methods=["GET"],
            response_model=BaseResponseModel[List[ItemResponseViewModel]],
            summary="Get items by category",
            description="Retrieve items by category",
            operation_id="get_items_by_category_v1"
        )

        self.router.add_api_route(
            "/{item_id}/stock",
            self.update_item_stock,
            methods=["PUT"],
            response_model=BaseResponseModel[ItemResponseViewModel],
            summary="Update item stock",
            description="Update item stock quantity",
            operation_id="update_item_stock_v1"
        )

        self.router.add_api_route(
            "/calculate-value",
            self.calculate_total_value,
            methods=["POST"],
            response_model=BaseResponseModel[ItemValueResponseViewModel],
            summary="Calculate item value",
            description="Calculate total value based on price and quantity",
            operation_id="calculate_total_value_v1"
        )

        self.router.add_api_route(
            "/calculate-discount",
            self.calculate_discount,
            methods=["POST"],
            response_model=BaseResponseModel[ItemDiscountResponseViewModel],
            summary="Calculate discount",
            description="Calculate discounted price based on original price and discount percentage",
            operation_id="calculate_discount_v1"
        )

        self.router.add_api_route(
            "/{item_id}",
            self.update_item,
            methods=["PUT"],
            response_model=BaseResponseModel[ItemResponseViewModel],
            summary="Update item",
            description="Update item details",
            operation_id="update_item_v1"
        )

        self.router.add_api_route(
            "/{item_id}",
            self.delete_item,
            methods=["DELETE"],
            response_model=BaseResponseModel[MessageResponseViewModel],
            summary="Delete item",
            description="Delete an item by ID",
            operation_id="delete_item_v1"
        )

    async def get_item(
            self,
            item_id: int
    ) -> SuccessResponseModel:
        """
        Get an item by ID.
        
        Args:
            item_id: The ID of the item to retrieve
            
        Returns:
            SuccessResponseModel: The retrieved item
        """
        item = await self.item_service.get(item_id)
        return SuccessResponseModel(
            message="Item retrieved successfully",
            data=item
        )

    async def create_item(
            self,
            item: ItemRequestViewModel
    ) -> SuccessResponseModel:
        """
        Create a new item.
        
        Args:
            item: The item data
            
        Returns:
            SuccessResponseModel: The created item
        """
        created_item = await self.item_service.create(item)
        return SuccessResponseModel(
            message="Item created successfully",
            data=created_item
        )

    async def get_items_by_category(
            self,
            category: str
    ) -> SuccessResponseModel:
        """
        Get items by category.
        
        Args:
            category: The category of items to retrieve
            
        Returns:
            SuccessResponseModel: The retrieved items
        """
        items = await self.item_service.get_by_category(category)
        return SuccessResponseModel(
            message=f"Items in category '{category}' retrieved successfully",
            data=items
        )

    async def update_item_stock(
            self,
            item_id: int,
            update: ItemStockUpdateViewModel
    ) -> SuccessResponseModel:
        """
        Update item stock.
        
        Args:
            item_id: The ID of the item to update
            update: The update data containing quantity
            
        Returns:
            SuccessResponseModel: The updated item
        """
        updated_item = await self.item_service.update_stock(item_id, update.quantity)
        return SuccessResponseModel(
            message="Item stock updated successfully",
            data=updated_item
        )

    async def calculate_total_value(
            self,
            price: float,
            quantity: int
    ) -> SuccessResponseModel:
        """
        Calculate total value.
        
        Args:
            price: The price of the item
            quantity: The quantity of items
            
        Returns:
            SuccessResponseModel: The calculation result
        """
        total_value = await self.item_service.calculate_total_value(price, quantity)
        result = ItemValueResponseViewModel(item_id=0, quantity=quantity, total_value=total_value)
        return SuccessResponseModel(
            message="Total value calculated successfully",
            data=result
        )

    async def calculate_discount(
            self,
            price: float,
            discount_percentage: float
    ) -> SuccessResponseModel:
        """
        Calculate discount.
        
        Args:
            price: The original price
            discount_percentage: The discount percentage
            
        Returns:
            SuccessResponseModel: The calculation result
        """
        final_price = await self.item_service.calculate_discount(price, discount_percentage)
        result = ItemDiscountResponseViewModel(
            item_id=0,
            original_price=price,
            discount_percentage=discount_percentage,
            final_price=final_price
        )
        return SuccessResponseModel(
            message="Discount calculated successfully",
            data=result
        )

    async def update_item(
            self,
            item_id: int,
            item: ItemRequestViewModel
    ) -> SuccessResponseModel:
        """
        Update an item.
        
        Args:
            item_id: The ID of the item to update
            item: The updated item data
            
        Returns:
            SuccessResponseModel: The updated item
        """
        item.id = item_id
        updated_item = await self.item_service.update(item)
        return SuccessResponseModel(
            message="Item updated successfully",
            data=updated_item
        )

    async def delete_item(
            self,
            item_id: int
    ) -> SuccessResponseModel:
        """
        Delete an item.
        
        Args:
            item_id: The ID of the item to delete
            
        Returns:
            SuccessResponseModel: Confirmation message
        """
        await self.item_service.delete(item_id)
        return SuccessResponseModel(
            message=f"Item with id {item_id} has been deleted",
            data={"message": f"Item with id {item_id} has been deleted"}
        )
