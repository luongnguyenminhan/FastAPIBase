from app.services.utils.example_core import MathOperations
from app.unit_of_work.unit_of_work import UnitOfWork

class MathService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.math_ops = MathOperations()

    @staticmethod
    def get_self(uow: UnitOfWork):
        return MathService(uow)
    
    async def calculate_operation(self, operation: str, x: float, y: float) -> float:
        operations = {
            'add': MathOperations.add,
            'subtract': MathOperations.subtract,
            'multiply': MathOperations.multiply,
            'divide': MathOperations.divide,
            'power': MathOperations.power
        }
        
        if operation not in operations:
            raise ValueError(f"Unsupported operation: {operation}")
            
        return operations[operation](x, y)
