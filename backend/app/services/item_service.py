from .base_service import BaseService
from app.repositories.item_repository import ItemRepository
from app.db.models import Item  # Updated import

class ItemService(BaseService[Item]):
    def __init__(self, repository: ItemRepository):
        super().__init__(repository)

    async def get_by_owner(self, owner_id: int):
        return self.repository.get_by_owner(owner_id)

    async def get_by_category(self, category: str):
        return self.repository.get_by_category(category)

    async def update_stock(self, id: int, quantity: int):
        return self.repository.update_stock(id, quantity)
