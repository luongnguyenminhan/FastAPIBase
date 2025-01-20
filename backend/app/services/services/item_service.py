from .base_service import BaseService
from app.db.models.items import Item
from app.services.utils.example_core import MathOperations
from app.unit_of_work.unit_of_work import UnitOfWork

class ItemService(BaseService[Item]):
    def __init__(self, uow: UnitOfWork):
        super().__init__(uow)
        self.item_repository = uow.item_repository
        self.user_repository = uow.user_repository

    @staticmethod
    def get_self(uow: UnitOfWork):
        return ItemService(uow)

    async def get_by_owner(self, owner_id: int):
        user = self.user_repository.get(owner_id)
        if not user:
            raise ValueError("Owner not found")
        return self.item_repository.get_by_owner(owner_id)

    async def get_by_category(self, category: str):
        return self.item_repository.get_by_category(category)

    async def update_stock(self, id: int, quantity: int):
        return self.item_repository.update_stock(id, quantity)

    async def calculate_total_value(self, price: float, quantity: int) -> float:
        """Calculate total value of items using math operations"""
        return MathOperations.multiply(price, quantity)

    async def calculate_discount(self, price: float, discount_percentage: float) -> float:
        """Calculate discounted price"""
        discount = MathOperations.multiply(price, MathOperations.divide(discount_percentage, 100))
        return MathOperations.subtract(price, discount)
