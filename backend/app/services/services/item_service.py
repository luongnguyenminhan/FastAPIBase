from fastapi import HTTPException, status, Depends
from .base_service import BaseService, service_method
from app.db.models import Item
from app.repositories.item_repository import ItemRepository
from app.services.utils.example_core import MathOperations
from app.unit_of_work.unit_of_work import UnitOfWork
from sqlalchemy.orm import Session
from backend.app.db.base import get_db

class ItemService(BaseService[Item]):
    repository_type = ItemRepository

    def __init__(self, uow: UnitOfWork):
        super().__init__(uow)

    @service_method
    async def get_by_owner(self, owner_id: int):
        user = await self.uow.user_repository.get_by_id_async(owner_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Owner with id {owner_id} not found"
            )
        return await self.repository.get_by_owner(owner_id)

    @service_method
    async def get_by_category(self, category: str):
        return await self.repository.get_by_category(category)

    @service_method
    async def update_stock(self, id: int, quantity: int):
        return await self.repository.update_stock(id, quantity)

    @service_method
    async def calculate_total_value(self, price: float, quantity: int) -> float:
        return MathOperations.multiply(price, quantity)

    @service_method
    async def calculate_discount(self, price: float, discount_percentage: float) -> float:
        discount = MathOperations.multiply(price, MathOperations.divide(discount_percentage, 100))
        return MathOperations.subtract(price, discount)

    @staticmethod
    def get_self(db: Session = Depends(get_db)):
        uow = UnitOfWork(db)
        return ItemService(uow)
