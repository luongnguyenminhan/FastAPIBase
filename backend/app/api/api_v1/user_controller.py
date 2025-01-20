from fastapi import APIRouter, Depends
from typing import List, Dict
from app.services.services.user_service import UserService
from app.schemas.response_schema import ItemResponse, UserResponse, MessageResponse
from app.schemas.request_schema import UserRequest

user_router = APIRouter()


# User endpoints
@user_router.get("/{user_id}", response_model=UserResponse, operation_id="get_user_v1")
async def get_user(
        user_id: int,
        user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get(user_id)


@user_router.get("/email/{email}", response_model=UserResponse, operation_id="get_user_by_email_v1")
async def get_user_by_email(
        email: str,
        user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get_by_email(email)


@user_router.get("/{user_id}/items", response_model=List[ItemResponse], operation_id="get_user_items_v1")
async def get_user_items(
        user_id: int,
        user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get_user_items(user_id)


@user_router.get("/active", response_model=List[UserResponse], operation_id="get_active_users_v1")
async def get_active_users(
        user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.get_active_users()


@user_router.post("/metrics", response_model=Dict[str, float], operation_id="calculate_user_metrics_v1")
async def calculate_user_metrics(
        metric_values: List[float],
        user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.calculate_user_metrics(metric_values)


@user_router.post("/", response_model=UserResponse, operation_id="create_user_v1")
async def create_user(
        user: UserRequest,
        user_service: UserService = Depends(UserService.get_self)
):
    return await user_service.create(user)


@user_router.put("/{user_id}", response_model=UserResponse, operation_id="update_user_v1")
async def update_user(
        user_id: int,
        user: UserRequest,
        user_service: UserService = Depends(UserService.get_self)
):
    user.id = user_id
    return await user_service.update(user)


@user_router.delete("/{user_id}", response_model=MessageResponse, operation_id="delete_user_v1")
async def delete_user(
        user_id: int,
        user_service: UserService = Depends(UserService.get_self)
):
    await user_service.delete(user_id)
    return {"message": f"User with id {user_id} has been deleted"}
