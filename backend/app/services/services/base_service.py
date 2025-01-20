from abc import abstractmethod
from typing import Generic, TypeVar, Callable, Type
from functools import wraps
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.unit_of_work.unit_of_work import UnitOfWork
from app.repositories.base_repository import BaseRepository
from app.db.base import get_db

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

    @staticmethod
    @abstractmethod
    def get_self(db: Session = Depends(get_db)):
        raise NotImplementedError("Subclasses must implement this method")
