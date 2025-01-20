from .base_repository import BaseRepository
from app.db.models.items import Item
from sqlalchemy.orm import Session

class ItemRepository(BaseRepository[Item]):
    def __init__(self, db: Session):
        super().__init__(Item, db)

    def get_by_owner(self, owner_id: int):
        return self._dbSet.filter_by(owner_id=owner_id, is_deleted=False).all()
    
    def get_by_category(self, category: str):
        return self._dbSet.filter_by(category=category, is_deleted=False).all()
    
    def update_stock(self, id: int, quantity: int):
        item = self.get_by_id(id)
        if item:
            item.stock = quantity
            self.update(item)
            return item.stock
        return None