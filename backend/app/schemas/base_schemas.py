from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal

class UserBase(BaseModel):
    email: str
    name: str
    is_active: Optional[bool] = True

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: Decimal
    category: Optional[str] = None
    is_active: bool = True
    stock: int = 0
