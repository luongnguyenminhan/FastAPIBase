from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from decimal import Decimal

# Math Operation Request
class MathOperationRequest(BaseModel):
    x: float = Field(..., description="First number")
    y: float = Field(..., description="Second number")

# User related requests
class UserRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    is_active: Optional[bool] = True

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "secretpassword",
                "is_active": True
            }
        }

class UserMetricsRequest(BaseModel):
    metric_values: List[float] = Field(..., description="List of metric values to calculate")

# Item related requests
class ItemRequest(BaseModel):
    title: str
    description: Optional[str] = None
    price: Decimal
    category: Optional[str] = None
    is_active: bool = True
    stock: int = 0
    owner_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Sample Item",
                "description": "A sample item description",
                "price": "29.99",
                "category": "electronics",
                "stock": 100,
                "owner_id": 1
            }
        }

class ItemUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None
    stock: Optional[int] = None

class ItemStockUpdateRequest(BaseModel):
    quantity: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "quantity": 10
            }
        }

class ItemDiscountRequest(BaseModel):
    price: float = Field(..., gt=0, description="Original price")
    discount_percentage: float = Field(..., ge=0, le=100, description="Discount percentage")
