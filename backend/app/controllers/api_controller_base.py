from fastapi import HTTPException
from functools import wraps
from typing import Callable, Any
from app.controllers.base_controller import BaseController
from app.unit_of_work.unit_of_work import UnitOfWork

def get_uow():
    uow = UnitOfWork()
    try:
        yield uow
    finally:
        uow.close()

def handle_exceptions(func: Callable) -> Callable:
    """Common exception handler decorator for API methods"""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper

class APIControllerBase(BaseController):
    """Base controller for all API versions"""
    pass
