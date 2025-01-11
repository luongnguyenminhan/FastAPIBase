from typing import Generic, TypeVar
from app.repositories.base_repository import BaseRepository

T = TypeVar('T')

class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    def get(self, id: int):
        return self.repository.get(id)

    def get_all(self):
        return self.repository.get_all()

    def create(self, obj_in):
        return self.repository.create(obj_in)
