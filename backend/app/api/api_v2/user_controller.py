from fastapi import APIRouter, Depends
from typing import List
from app.services.services.user_service import UserService
from app.schemas.response_schema import UserResponse, UserMetricsResponse
from app.schemas.request_schema import UserMetricsRequest

user_router = APIRouter()

# Advanced User endpoints
@user_router.get("/active", response_model=List[UserResponse], operation_id="get_active_users_v2")
async def get_active_users(
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get_active_users()

@user_router.post("/metrics", response_model=UserMetricsResponse, operation_id="calculate_user_metrics_v2")
async def calculate_user_metrics(
    request: UserMetricsRequest,
    user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.calculate_user_metrics(request.metric_values)
