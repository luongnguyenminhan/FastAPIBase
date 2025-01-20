from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, List
from sqlalchemy.future import select
from datetime import datetime
from app.schemas.common import PaginationParameter, Pagination
from app.db.models.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db
        self._dbSet = db.query(model)

    def get_by_id(self, id: int) -> T:
        return self._dbSet.filter_by(id=id, is_deleted=False).first()

    def get_all(self) -> List[T]:
        return self._dbSet.filter_by(is_deleted=False).all()

    def add(self, entity: T) -> T:
        entity.create_date = datetime.utcnow()
        self.db.add(entity)
        self.db.flush()
        return entity

    def add_range(self, entities: List[T]):
        current_time = datetime.utcnow()
        for entity in entities:
            entity.create_date = current_time
        self.db.add_all(entities)
        self.db.flush()

    def update(self, entity: T):
        entity.update_date = datetime.utcnow()
        self._dbSet.update(entity)

    def soft_delete(self, entity: T):
        entity.is_deleted = True
        self._dbSet.update(entity)

    def soft_delete_range(self, entities: List[T]):
        for entity in entities:
            entity.is_deleted = True
        self._dbSet.update(entities)

    def permanent_delete(self, entity: T):
        self.db.delete(entity)

    def permanent_delete_list(self, entities: List[T]):
        for entity in entities:
            self.db.delete(entity)

    def to_pagination(self, pagination_parameter: PaginationParameter) -> Pagination[T]:
        query = self._dbSet.filter_by(is_deleted=False)
        
        # Get total count
        total_count = query.count()

        # Get paginated items
        items = query.offset(
            (pagination_parameter.page_index - 1) * pagination_parameter.page_size
        ).limit(pagination_parameter.page_size).all()

        return Pagination(
            items=items,
            total_count=total_count,
            page_index=pagination_parameter.page_index,
            page_size=pagination_parameter.page_size
        )
