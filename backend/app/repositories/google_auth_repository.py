import logging
from typing import Optional

from backend.app.db.models.base_model import Users
from backend.app.repositories.base_repository import BaseRepository
from backend.app.repositories.repository_interface.i_google_auth_repository import IGoogleAuthRepository
from backend.app.schemas.user import UserCreate

logger = logging.getLogger(__name__)


class GoogleAuthRepository(BaseRepository[Users], IGoogleAuthRepository):
    def __init__(self, db):
        super().__init__(Users, db)
        logger.info("GoogleAuthRepository initialized")

    async def get_user_by_google_email(self, google_email: str) -> Optional[Users]:
        """Get a user by Google email."""
        logger.debug(f"Getting user by google_email: {google_email}")
        return self._dbSet.filter_by(google_email=google_email, is_deleted=False).first()

    async def create_user_from_google(self, user_data: UserCreate) -> Users:
        """Create a new user from Google sign-in data."""
        logger.debug(f"Creating user with google_email: {user_data.google_email}")
        new_user = Users(
            google_email=user_data.google_email,
            display_name=user_data.display_name,
            avatar_url=user_data.avatar_url,
            role='user'  # Default role
        )
        return self.add(new_user)
