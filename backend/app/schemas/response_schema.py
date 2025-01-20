from pydantic import BaseModel
from typing import List, Optional

class MessageResponse(BaseModel):
    message: str

class EchoResponse(BaseModel):
    echo: str
    version: str

class MathOperationResponse(BaseModel):
    operation: str
    result: float

class UserMetricsResponse(BaseModel):
    total: float
    average: float

class ItemValueResponse(BaseModel):
    total_value: float

class ItemDiscountResponse(BaseModel):
    original_price: float
    discount_percentage: float
    discounted_price: float
