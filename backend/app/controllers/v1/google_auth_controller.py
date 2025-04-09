import logging

from backend.app.services.utils.exceptions.exceptions import APIException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.base import get_db
from backend.app.schemas.user import GoogleTokenRequest, AuthResponse
from backend.app.services.services.google_auth_service import GoogleAuthService
from backend.app.unit_of_work.unit_of_work import UnitOfWork
from backend.app.schemas.business_model.response_base import BaseResponseModel, ErrorResponseModel, SuccessResponseModel

logger = logging.getLogger(__name__)


class GoogleAuthController:
    """Controller for handling Google Authentication endpoints."""

    def __init__(self, router: APIRouter, db: Session = Depends(get_db)):
        """Initializes the GoogleAuthController."""
        self.router = router
        self.auth_service = GoogleAuthService(UnitOfWork(db))
        self._register_routes()

    def _register_routes(self) -> None:
        """Registers the Google login route."""
        self.router.add_api_route(
            "/google",
            self.google_login,
            methods=["POST"],
            response_model=BaseResponseModel[AuthResponse],
            summary="Login with Google",
            description="Authenticates a user with a Google ID token. If the user doesn't exist, they are created.",
            operation_id="google_login_v1",
        )

    async def google_login(
        self, token_request: GoogleTokenRequest
    ) -> SuccessResponseModel:
        """Authenticates a user with a Google ID token."""
        try:
            auth_response: AuthResponse = await self.auth_service.process_google_login(token_request.id_token)
            return SuccessResponseModel(
                message="Google login successful",
                data=auth_response,
            )
        except Exception as e:
            logger.exception("Google login failed")
            raise APIException(
                status_code=500,
                error_code="GOOGLE_LOGIN_FAILED",
                message=str(e),
            )


# Create router instance
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Initialize the controller and register routes
GoogleAuthController(router=router)
