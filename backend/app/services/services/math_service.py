from app.unit_of_work.unit_of_work import UnitOfWork
from app.services.utils.example_core import MathOperations
from .base_service import service_method
from fastapi import HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.db.base import get_db

class MathService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.operations = {
            'add': MathOperations.add,
            'subtract': MathOperations.subtract,
            'multiply': MathOperations.multiply,
            'divide': MathOperations.divide,
            'power': MathOperations.power
        }

    @staticmethod
    def get_self(db: Session = Depends(get_db)):
        uow = UnitOfWork(db)
        return MathService(uow)
    
    @service_method
    async def calculate_operation(self, operation: str, x: float, y: float) -> float:
        if operation not in self.operations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported operation: {operation}"
            )
        return self.operations[operation](x, y)
