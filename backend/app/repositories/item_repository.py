from .base_repository import BaseRepository
from app.db.models.items import Item
from sqlalchemy.orm import Session

class ItemRepository(BaseRepository[Item]):
    def __init__(self, db: Session):
        super().__init__(Item, db)
