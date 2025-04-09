import logging
from typing import Optional

from google.auth.transport import requests
from google.oauth2 import id_token
from jose import jwt, JWTError
from datetime import datetime, timedelta

from backend.app.core.config import settings
from backend.app.db.models.base_model import Users
from backend.app.repositories.repository_interface.i_google_auth_repository import IGoogleAuthRepository
from backend.app.schemas.user import UserCreate, AuthResponse, UserResponse
from backend.app.services.service_interface.i_google_auth_service import IGoogleAuthService
from backend.app.services.utils.exceptions.exceptions import CredentialsException, ServiceException
from backend.app.unit_of_work.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


class GoogleAuthService(IGoogleAuthService):
    """Service layer for handling Google Authentication."""

    def __init__(self, uow: UnitOfWork):
        """Initializes the GoogleAuthService."""
        self.uow: UnitOfWork = uow
        self.google_auth_repo: IGoogleAuthRepository = uow.google_auth_repository
        logger.info("GoogleAuthService initialized")

    async def verify_google_token(self, token: str) -> Optional[dict]:
        """Verifies the Google ID token and returns the payload."""
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )
            logger.info(f"Google token verified for email: {idinfo.get('email')}")
            return idinfo
        except ValueError as e:
            # Invalid token
            logger.error(f"Google token verification failed: {str(e)}")
            raise CredentialsException("Invalid Google token")
        except Exception as e:
            logger.error(f"An unexpected error occurred during token verification: {str(e)}")
            raise ServiceException("Token verification failed")

    async def authenticate_or_create_user(self, token_payload: dict) -> Users:
        """Authenticates an existing user or creates a new one based on token payload."""
        google_email: Optional[str] = token_payload.get("email")
        if not google_email:
            logger.error("Email not found in Google token payload")
            raise CredentialsException("Email not found in token")

        try:
            async with self.uow.transaction():
                user = await self.google_auth_repo.get_user_by_google_email(google_email)
                if user:
                    logger.info(f"User found with email: {google_email}")
                    # Optionally update user details like display name or avatar here if needed
                    # user.display_name = token_payload.get("name")
                    # user.avatar_url = token_payload.get("picture")
                    # await self.google_auth_repo.update(user) # Assuming update method exists
                else:
                    logger.info(f"Creating new user for email: {google_email}")
                    user_data = UserCreate(
                        google_email=google_email,
                        display_name=token_payload.get("name", ""), # Provide default if missing
                        avatar_url=token_payload.get("picture")
                    )
                    user = await self.google_auth_repo.create_user_from_google(user_data)
                await self.uow.commit() # Use await for async commit if applicable
                return user
        except Exception as e:
            logger.error(f"Database error during user authentication/creation: {str(e)}")
            await self.uow.rollback() # Use await for async rollback if applicable
            raise ServiceException("Could not process user data")

    async def create_access_token(self, user: Users) -> AuthResponse:
        """Creates an access token (JWT) for the given user."""
        to_encode = {
            "sub": str(user.id), # Subject claim (user ID)
            "email": user.google_email,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        try:
            encoded_jwt: str = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            logger.info(f"Access token created for user ID: {user.id}")
            user_response = UserResponse.model_validate(user)
            return AuthResponse(access_token=encoded_jwt, user=user_response)
        except JWTError as e:
            logger.error(f"Error encoding JWT: {str(e)}")
            raise ServiceException("Could not create access token")

    async def process_google_login(self, id_token_str: str) -> AuthResponse:
        """Handles the complete Google login flow."""
        logger.info("Processing Google login")
        token_payload = await self.verify_google_token(id_token_str)
        if not token_payload:
            # Verification already raised an exception
            # This path should ideally not be reached if exceptions are handled
            raise CredentialsException("Token verification failed internally")

        user = await self.authenticate_or_create_user(token_payload)
        auth_response = await self.create_access_token(user)
        logger.info(f"Google login processed successfully for user ID: {user.id}")
        return auth_response
