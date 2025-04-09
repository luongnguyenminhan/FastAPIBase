from abc import ABC, abstractmethod
from typing import Optional

from backend.app.db.models.base_model import Users
from backend.app.schemas.user import UserCreate, AuthResponse


class IGoogleAuthService(ABC):

    @abstractmethod
    async def verify_google_token(self, id_token: str) -> Optional[dict]:
        """Verifies the Google ID token and returns the payload."""
        pass

    @abstractmethod
    async def authenticate_or_create_user(self, token_payload: dict) -> Users:
        """Authenticates an existing user or creates a new one based on token payload."""
        pass

    @abstractmethod
    async def create_access_token(self, user: Users) -> AuthResponse:
        """Creates an access token for the given user."""
        pass

    @abstractmethod
    async def process_google_login(self, id_token: str) -> AuthResponse:
        """Handles the complete Google login flow."""
        pass
