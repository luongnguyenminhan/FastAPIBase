from .base_service import BaseService
from app.repositories.user_repository import UserRepository
from app.db.models import User  # Updated import

class UserService(BaseService[User]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    async def get_by_email(self, email: str):
        return self.repository.get_by_email(email)

    async def get_active_users(self):
        return self.repository.get_active_users()
