from fastapi import APIRouter

from .google_auth_controller import router as google_auth_router


router = APIRouter(prefix="/v1")
router.include_router(google_auth_router)
