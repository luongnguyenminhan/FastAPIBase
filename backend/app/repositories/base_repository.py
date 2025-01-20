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

    async def get_by_id_async(self, id: int) -> T:
        result = await self.db.execute(
            select(self.model).filter_by(id=id, is_deleted=False)
        )
        return result.scalar_one_or_none()

    async def get_all_async(self) -> List[T]:
        result = await self.db.execute(
            select(self.model).filter_by(is_deleted=False)
        )
        return result.scalars().all()

    async def add_async(self, entity: T) -> T:
        entity.create_date = datetime.utcnow()
        self.db.add(entity)
        await self.db.flush()
        return entity

    async def add_range_async(self, entities: List[T]):
        current_time = datetime.utcnow()
        for entity in entities:
            entity.create_date = current_time
        self.db.add_all(entities)
        await self.db.flush()

    def update_async(self, entity: T):
        entity.update_date = datetime.utcnow()
        self._dbSet.update(entity)

    def soft_delete_async(self, entity: T):
        entity.is_deleted = True
        self._dbSet.update(entity)

    def soft_delete_range_async(self, entities: List[T]):
        for entity in entities:
            entity.is_deleted = True
        self._dbSet.update(entities)

    def permanent_delete_async(self, entity: T):
        self.db.delete(entity)

    def permanent_delete_list_async(self, entities: List[T]):
        for entity in entities:
            self.db.delete(entity)

    async def to_pagination(self, pagination_parameter: PaginationParameter) -> Pagination[T]:
        query = select(self.model).filter_by(is_deleted=False)
        
        # Get total count
        count_result = await self.db.execute(select(func.count()).select_from(query))
        total_count = count_result.scalar()

        # Get paginated items
        items_query = query.offset(
            (pagination_parameter.page_index - 1) * pagination_parameter.page_size
        ).limit(pagination_parameter.page_size)
        
        result = await self.db.execute(items_query)
        items = result.scalars().all()

        return Pagination(
            items=items,
            total_count=total_count,
            page_index=pagination_parameter.page_index,
            page_size=pagination_parameter.page_size
        )
