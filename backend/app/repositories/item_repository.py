from .base_repository import BaseRepository
from app.db.models.items import Item
from sqlalchemy.orm import Session
from typing import List

class ItemRepository(BaseRepository[Item]):
    def __init__(self, db: Session):
        super().__init__(Item, db)
    
    def get_by_category(self, category: str) -> List[Item]:
        return self.db.query(self.model).filter(self.model.category == category).all()
    
    def get_available_Items(self) -> List[Item]:
        return self.db.query(self.model).filter(self.model.stock > 0).all()
    
    def get_by_owner(self, owner_id: int) -> List[Item]:
        return self.db.query(self.model).filter(self.model.owner_id == owner_id).all()
    
    def update_stock(self, id: int, quantity: int):
        Item = self.get(id)
        if Item:
            Item.stock += quantity
            self.db.commit()
        return Item
    
    def delete(self, id: int):
        Item = self.get(id)
        if Item:
            self.db.delete(Item)
            self.db.commit()
        return Item
