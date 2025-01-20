from .base_service import BaseService
from app.db.models import User
from app.services.utils.example_core import MathOperations
from app.unit_of_work.unit_of_work import UnitOfWork

class UserService(BaseService[User]):
    def __init__(self, uow: UnitOfWork):
        super().__init__(uow)
        self.user_repository = uow.user_repository
        self.item_repository = uow.item_repository

    @staticmethod
    def get_self(uow: UnitOfWork):
        return UserService(uow)

    async def get_by_email(self, email: str):
        return self.user_repository.get_by_email(email)

    async def get_active_users(self):
        return self.user_repository.get_active_users()

    async def get_user_items(self, user_id: int):
        return self.item_repository.get_by_owner(user_id)

    async def calculate_user_metrics(self, metric_values: list[float]) -> dict:
        """Calculate various user metrics using math operations"""
        if not metric_values:
            return {"total": 0, "average": 0}
            
        total = sum(metric_values)
        average = total / len(metric_values)
        
        return {
            "total": total,
            "average": average
        }
