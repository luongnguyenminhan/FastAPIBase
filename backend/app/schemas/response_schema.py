from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

# Generic responses
class MessageResponse(BaseModel):
    message: str

class EchoResponse(BaseModel):
    echo: str
    version: str

# User related responses
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    items_count: int = 0

    class Config:
        from_attributes = True

class UserMetricsResponse(BaseModel):
    total: float
    average: float

# Item related responses
class ItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: Decimal
    category: Optional[str]
    is_active: bool
    stock: int
    owner_id: int

    class Config:
        from_attributes = True

class ItemWithOwnerResponse(ItemResponse):
    owner: Optional[UserResponse] = None

class ItemValueResponse(BaseModel):
    item_id: int
    quantity: int
    total_value: Decimal

class ItemDiscountResponse(BaseModel):
    item_id: int
    original_price: Decimal
    discount_percentage: float
    final_price: Decimal
