from abc import abstractmethod
from typing import Generic, TypeVar, Callable, Type
from functools import wraps
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.unit_of_work.unit_of_work import UnitOfWork
from app.repositories.base_repository import BaseRepository
from backend.app.db.base import get_db

T = TypeVar('T')

def service_method(func: Callable):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    return wrapper

class BaseService(Generic[T]):
    repository_type: Type[BaseRepository] = None  # Subclasses must set this

    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        if not self.repository_type:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Service must define repository_type"
            )
            
    @service_method
    async def get(self, id: int):
        return await self.repository.get_by_id_async(id)

    @service_method
    async def get_all(self):
        return await self.repository.get_all_async()

    @service_method
    async def create(self, obj_in):
        result = await self.repository.add_async(obj_in)
        self.uow.save()
        return result

    @service_method
    async def update(self, id: int, obj_in):
        result = await self.repository.update_async(obj_in)
        self.uow.save()
        return result

    @service_method
    async def delete(self, id: int):
        entity = await self.get(id)
        if entity:
            return await self.repository.soft_delete_async(entity)
        self.uow.save()
        return None

    @staticmethod
    @abstractmethod
    def get_self(db: Session = Depends(get_db)):
        raise NotImplementedError("Subclasses must implement this method")
