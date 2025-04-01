"""
API V2 Router Configuration

This file configures the main API v2 router and initializes all v2 controllers.
It follows a controller-based architecture pattern.

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.1.0
"""

from fastapi import APIRouter
from app.controllers.v2.user_controller import UserController
from app.controllers.v2.item_controller import ItemController
from app.controllers.v2.math_controller import MathController

# Create main API router for v2
api_router = APIRouter()

# Create sub-routers for each resource type
users_router = APIRouter()
items_router = APIRouter()
math_router = APIRouter()

# Initialize controllers with their respective routers
user_controller = UserController(users_router)
item_controller = ItemController(items_router)
math_controller = MathController(math_router)

# Include the sub-routers in the main API router
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(items_router, prefix="/items", tags=["Items"])
api_router.include_router(math_router, prefix="/math", tags=["Math"])

# Export the router for use in the main application
__all__ = ["api_router"]