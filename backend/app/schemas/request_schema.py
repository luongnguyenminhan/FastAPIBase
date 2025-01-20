from pydantic import BaseModel, Field
from typing import List

class MathOperationRequest(BaseModel):
    x: float = Field(..., description="First number")
    y: float = Field(..., description="Second number")

class UserMetricsRequest(BaseModel):
    metric_values: List[float] = Field(..., description="List of metric values to calculate")

class ItemValueRequest(BaseModel):
    price: float = Field(..., gt=0, description="Item price")
    quantity: int = Field(..., gt=0, description="Item quantity")

class ItemDiscountRequest(BaseModel):
    price: float = Field(..., gt=0, description="Original price")
    discount_percentage: float = Field(..., ge=0, le=100, description="Discount percentage")
