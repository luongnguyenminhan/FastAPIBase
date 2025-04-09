"""
User and Authentication Schema Exports

This file re-exports user and authentication-related schemas from business and view models.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl

# --- Base Models (Can be in business_model/base.py or common.py if reused) ---

class UserBase(BaseModel):
    """Base Pydantic model for User data, shared attributes."""
    google_email: EmailStr
    display_name: str
    avatar_url: Optional[HttpUrl] = None

    class Config:
        from_attributes = True # Allow creating from ORM model

# --- Business Logic / Service Layer Schemas (Can be in business_model) ---

class UserCreate(UserBase):
    """Schema for creating a user via Google Auth."""
    pass # Inherits all fields from UserBase

class UserUpdate(BaseModel):
    """Schema for updating user information (example)."""
    display_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None

# --- Database Model Representation (Mirrors DB model, often used internally) ---

class UserInDB(UserBase):
    """Schema representing a User as stored in the database."""
    id: int
    role: str
    create_date: datetime
    update_date: Optional[datetime] = None
    is_deleted: bool

# --- API Request/Response Schemas (in view_model) ---

# Request Schemas

class GoogleTokenRequest(BaseModel):
    """Schema for receiving the Google ID token."""
    id_token: str

# Response Schemas

class UserResponse(UserBase):
    """Schema for API responses containing user information."""
    id: int
    role: str

class AuthResponse(BaseModel):
    """Schema for authentication responses (e.g., JWT token)."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# --- Exporting Schemas for Use --- #
__all__ = [
    'UserBase',
    'UserCreate',
    'UserUpdate',
    'UserInDB',
    'GoogleTokenRequest',
    'UserResponse',
    'AuthResponse'
]
