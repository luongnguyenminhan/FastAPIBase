from .base_service import BaseService, service_method
from app.db.models import User
from app.repositories.user_repository import UserRepository
from app.unit_of_work.unit_of_work import UnitOfWork
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db

class UserService(BaseService[User]):

    def __init__(self, uow: UnitOfWork):
        super().__init__(uow)

    @staticmethod
    def get_self(db: Session = Depends(get_db)):
        uow = UnitOfWork(db)
        return UserService(uow)

    @service_method
    async def get_by_email(self, email: str):
        return self.uow.user_repository.get_by_email(email)

    @service_method
    async def get_active_users(self):
        return self.uow.user_repository.get_active_users()

    @service_method
    async def get_user_items(self, user_id: int):
        return self.uow.item_repository.get_by_owner(user_id)

    @service_method
    async def calculate_user_metrics(self, metric_values: list[float]) -> dict:
        if not metric_values:
            return {"total": 0, "average": 0}
        total = sum(metric_values)
        average = total / len(metric_values)
        return {"total": total, "average": average}

    @service_method
    async def get(self, id: int):
        user = self.uow.user_repository.get_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {id} not found"
            )
        return user
