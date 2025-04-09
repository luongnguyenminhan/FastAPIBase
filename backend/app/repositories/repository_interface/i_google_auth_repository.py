
from abc import abstractmethod
from typing import Optional

from backend.app.db.models.base_model import Users
from backend.app.repositories.repository_interface.i_base_repository import IBaseRepository
from backend.app.schemas.user import UserCreate


class IGoogleAuthRepository(IBaseRepository):
    @abstractmethod
    async def get_user_by_google_email(self, google_email: str) -> Optional[Users]:
        pass

    @abstractmethod
    async def create_user_from_google(self, user_data: UserCreate) -> Users:
        pass
