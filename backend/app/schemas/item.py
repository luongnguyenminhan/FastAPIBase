from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: Decimal
    category: Optional[str] = None
    is_active: bool = True
    stock: int = 0

class ItemCreate(ItemBase):
    owner_id: Optional[int] = None

class ItemUpdate(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None
    stock: Optional[int] = None
    owner_id: Optional[int] = None

class ItemInDB(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
