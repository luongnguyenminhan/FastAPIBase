from typing import Generic, TypeVar, Callable
from functools import wraps

T = TypeVar('T')

def service_method(func: Callable):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as e:
            raise e
    return wrapper

class BaseService(Generic[T]):
    def __init__(self, repository):
        self.repository = repository

    @service_method
    async def get(self, id: int):
        return self.repository.get(id)

    @service_method
    async def get_all(self):
        return self.repository.get_all()

    @service_method
    async def create(self, obj_in):
        return self.repository.create(obj_in)

    @service_method
    async def update(self, id: int, obj_in):
        return self.repository.update(id, obj_in)

    @service_method
    async def delete(self, id: int):
        return self.repository.delete(id)
