from typing import Type, TypeVar
from app.unit_of_work.unit_of_work import UnitOfWork
from app.services.services.base_service import BaseService

T = TypeVar('T', bound=BaseService)

class BaseController:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_service(self, service_class: Type[T]) -> T:
        """
        Get an instance of any service using its get_self static method
        """
        if not hasattr(service_class, 'get_self'):
            raise AttributeError(f"{service_class.__name__} must implement get_self static method")
        
        return service_class.get_self(self.uow)
