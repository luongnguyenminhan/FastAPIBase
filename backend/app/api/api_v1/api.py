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
from app.schemas.response_schema import UserResponse, ItemResponse, MessageResponse
from app.schemas.request_schema import UserRequest, ItemRequest, MathOperationRequest

api_router = APIRouter()  # Changed variable name to api_router

