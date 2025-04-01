"""
Item Controller V2

This file defines the ItemController class for handling item-related endpoints.
It follows the controller pattern to separate route definition from request handling logic.
This is the v2 version with enhanced features.

Author: Minh An
Last Modified: 23 Jun 2024
Version: 2.0.0
"""

from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.services.services.item_service import ItemService
from app.schemas.view_model.response import (
    ItemResponseViewModel,
    MessageResponseViewModel,
    ItemValueResponseViewModel,
    ItemDiscountResponseViewModel
)
from app.schemas.view_model.request import (
    ItemRequestViewModel,
    ItemStockUpdateViewModel
)
from app.schemas.business_model.response_base import BaseResponseModel, SuccessResponseModel


class ItemController:
    """
    Controller handling item-related endpoints including item retrieval,
    creation, updating, deletion, and calculations with enhanced features.
    """
    
    def __init__(self, router: APIRouter):
        self.router = router
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
            operation_id="get_item_v2"
        )
        
        self.router.add_api_route(
            "/",
            self.create_item,
            methods=["POST"],
            response_model=BaseResponseModel[ItemResponseViewModel],
            summary="Create item",
            description="Create a new item",
            operation_id="create_item_v2"
        )
        
        # Enhanced with pagination
        self.router.add_api_route(
            "/category/{category}",
            self.get_items_by_category,
            methods=["GET"],
            response_model=BaseResponseModel[List[ItemResponseViewModel]],
            summary="Get items by category",
            description="Retrieve items by category with pagination",
            operation_id="get_items_by_category_v2"
        )
        
        self.router.add_api_route(
            "/{item_id}/stock",
            self.update_item_stock,
            methods=["PUT"],
            response_model=BaseResponseModel[ItemResponseViewModel],
            summary="Update item stock",
            description="Update item stock quantity",
            operation_id="update_item_stock_v2"
        )
        
        # Enhanced with metadata
        self.router.add_api_route(
            "/calculate-value",
            self.calculate_total_value,
            methods=["POST"],
            response_model=BaseResponseModel[ItemValueResponseViewModel],
            summary="Calculate item value",
            description="Calculate total value based on price and quantity with tax information",
            operation_id="calculate_total_value_v2"
        )
        
        # Enhanced with additional options
        self.router.add_api_route(
            "/calculate-discount",
            self.calculate_discount,
            methods=["POST"],
            response_model=BaseResponseModel[ItemDiscountResponseViewModel],
            summary="Calculate discount",
            description="Calculate discounted price based on original price and discount percentage",
            operation_id="calculate_discount_v2"
        )
        
        self.router.add_api_route(
            "/{item_id}",
            self.update_item,
            methods=["PUT"],
            response_model=BaseResponseModel[ItemResponseViewModel],
            summary="Update item",
            description="Update item details",
            operation_id="update_item_v2"
        )
        
        self.router.add_api_route(
            "/{item_id}",
            self.delete_item,
            methods=["DELETE"],
            response_model=BaseResponseModel[MessageResponseViewModel],
            summary="Delete item",
            description="Delete an item by ID",
            operation_id="delete_item_v2"
        )
    
    async def get_item(
        self,
        item_id: int,
        item_service: ItemService = Depends(ItemService.get_self)
    ) -> SuccessResponseModel:
        """
        Get an item by ID.
        
        Args:
            item_id: The ID of the item to retrieve
            item_service: The item service for business logic
            
        Returns:
            SuccessResponseModel: The retrieved item
        """
        item = await item_service.get(item_id)
        return SuccessResponseModel(
            message="Item retrieved successfully",
            data=item
        )
    
    async def create_item(
        self,
        item: ItemRequestViewModel,
        item_service: ItemService = Depends(ItemService.get_self)
    ) -> SuccessResponseModel:
        """
        Create a new item.
        
        Args:
            item: The item data
            item_service: The item service for business logic
            
        Returns:
            SuccessResponseModel: The created item
        """
        created_item = await item_service.create(item)
        return SuccessResponseModel(
            message="Item created successfully",
            data=created_item
        )
    
    async def get_items_by_category(
        self,
        category: str,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        item_service: ItemService = Depends(ItemService.get_self)
    ) -> SuccessResponseModel:
        """
        Get items by category with pagination.
        
        Args:
            category: The category of items to retrieve
            skip: The number of items to skip
            limit: The maximum number of items to return
            item_service: The item service for business logic
            
        Returns:
            SuccessResponseModel: The retrieved items with pagination metadata
        """
        items = await item_service.get_by_category(category)
        
        # Apply pagination (in a real app, this would be done at the database level)
        paginated_items = items[skip:skip + limit]
        
        return SuccessResponseModel(
            message=f"Items in category '{category}' retrieved successfully",
            data=paginated_items,
            metadata={
                "total": len(items),
                "page": skip // limit + 1,
                "page_size": limit,
                "pages": (len(items) + limit - 1) // limit
            }
        )
    
    async def update_item_stock(
        self,
        item_id: int,
        update: ItemStockUpdateViewModel,
        item_service: ItemService = Depends(ItemService.get_self)
    ) -> SuccessResponseModel:
        """
        Update item stock.
        
        Args:
            item_id: The ID of the item to update
            update: The update data containing quantity
            item_service: The item service for business logic
            
        Returns:
            SuccessResponseModel: The updated item
        """
        updated_item = await item_service.update_stock(item_id, update.quantity)
        return SuccessResponseModel(
            message="Item stock updated successfully",
            data=updated_item
        )
    
    async def calculate_total_value(
        self,
        price: float,
        quantity: int,
        tax_rate: Optional[float] = Query(0.0, ge=0.0, le=1.0),
        item_service: ItemService = Depends(ItemService.get_self)
    ) -> SuccessResponseModel:
        """
        Calculate total value with tax information.
        
        Args:
            price: The price of the item
            quantity: The quantity of items
            tax_rate: The tax rate to apply (0.0 to 1.0)
            item_service: The item service for business logic
            
        Returns:
            SuccessResponseModel: The calculation result with tax information
        """
        total_value = await item_service.calculate_total_value(price, quantity)
        
        # Calculate tax amount
        tax_amount = total_value * tax_rate
        final_value = total_value + tax_amount
        
        result = ItemValueResponseViewModel(
            item_id=0, 
            quantity=quantity, 
            total_value=final_value
        )
        
        return SuccessResponseModel(
            message="Total value calculated successfully",
            data=result,
            metadata={
                "subtotal": total_value,
                "tax_rate": tax_rate,
                "tax_amount": tax_amount,
                "final_value": final_value
            }
        )
    
    async def calculate_discount(
        self,
        price: float,
        discount_percentage: float,
        apply_additional_discount: bool = False,
        item_service: ItemService = Depends(ItemService.get_self)
    ) -> SuccessResponseModel:
        """
        Calculate discount with optional additional discount.
        
        Args:
            price: The original price
            discount_percentage: The discount percentage
            apply_additional_discount: Whether to apply an additional 5% discount
            item_service: The item service for business logic
            
        Returns:
            SuccessResponseModel: The calculation result
        """
        final_price = await item_service.calculate_discount(price, discount_percentage)
        
        # Apply additional discount if requested
        additional_discount = 0.0
        if apply_additional_discount:
            additional_discount = final_price * 0.05
            final_price -= additional_discount
        
        result = ItemDiscountResponseViewModel(
            item_id=0,
            original_price=price,
            discount_percentage=discount_percentage,
            final_price=final_price
        )
        
        return SuccessResponseModel(
            message="Discount calculated successfully",
            data=result,
            metadata={
                "additional_discount_applied": apply_additional_discount,
                "additional_discount_amount": additional_discount,
                "total_discount_amount": price - final_price
            }
        )
    
    async def update_item(
        self,
        item_id: int,
        item: ItemRequestViewModel,
        item_service: ItemService = Depends(ItemService.get_self)
    ) -> SuccessResponseModel:
        """
        Update an item.
        
        Args:
            item_id: The ID of the item to update
            item: The updated item data
            item_service: The item service for business logic
            
        Returns:
            SuccessResponseModel: The updated item
        """
        item.id = item_id
        updated_item = await item_service.update(item)
        return SuccessResponseModel(
            message="Item updated successfully",
            data=updated_item
        )
    
    async def delete_item(
        self,
        item_id: int,
        item_service: ItemService = Depends(ItemService.get_self)
    ) -> SuccessResponseModel:
        """
        Delete an item.
        
        Args:
            item_id: The ID of the item to delete
            item_service: The item service for business logic
            
        Returns:
            SuccessResponseModel: Confirmation message
        """
        await item_service.delete(item_id)
        return SuccessResponseModel(
            message=f"Item with id {item_id} has been deleted",
            data={"message": f"Item with id {item_id} has been deleted"}
        )